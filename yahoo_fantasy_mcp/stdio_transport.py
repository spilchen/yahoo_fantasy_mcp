"""Custom stdio transport that shuts down cleanly on the first Ctrl+C."""

import codecs
import os
import sys
from contextlib import asynccontextmanager

import anyio
import anyio.lowlevel
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
import mcp.types as types
from mcp.shared.message import SessionMessage
from mcp.server.stdio import stdio_server


@asynccontextmanager
async def graceful_stdio_server():
    """Wrap mcp stdio transport but ensure stdin closes on shutdown."""
    if os.name == "nt":  # pragma: no cover - Windows fallback
        async with stdio_server() as streams:
            yield streams
        return

    stdin_buffer = getattr(sys.stdin, "buffer", sys.stdin)
    stdin_raw = getattr(stdin_buffer, "raw", stdin_buffer)
    stdin_fd = stdin_raw.fileno()
    stdout_buffer = getattr(sys.stdout, "buffer", sys.stdout)
    stdout_raw = getattr(stdout_buffer, "raw", stdout_buffer)
    stdout_fd = stdout_raw.fileno()
    decoder = codecs.getincrementaldecoder("utf-8")()
    pending_line = ""

    read_stream_writer, read_stream = anyio.create_memory_object_stream(0)
    write_stream, write_stream_reader = anyio.create_memory_object_stream(0)

    async def stdin_reader():
        nonlocal pending_line

        async def process_line(raw_line: str) -> None:
            line = raw_line.rstrip("\r")
            if not line:
                return

            try:
                message = types.JSONRPCMessage.model_validate_json(line)
            except Exception as exc:  # pragma: no cover
                await read_stream_writer.send(exc)
                return

            session_message = SessionMessage(message)
            await read_stream_writer.send(session_message)

        try:
            async with read_stream_writer:
                while True:
                    await anyio.wait_readable(stdin_fd)
                    try:
                        chunk = os.read(stdin_fd, 4096)
                    except BlockingIOError:  # pragma: no cover
                        continue

                    if not chunk:
                        pending_line += decoder.decode(b"", final=True)
                        if pending_line:
                            await process_line(pending_line)
                            pending_line = ""
                        break

                    pending_line += decoder.decode(chunk)
                    while True:
                        newline_index = pending_line.find("\n")
                        if newline_index == -1:
                            break
                        line = pending_line[:newline_index]
                        pending_line = pending_line[newline_index + 1 :]
                        await process_line(line)
        except (anyio.ClosedResourceError, OSError, ValueError):  # pragma: no cover
            await anyio.lowlevel.checkpoint()

    async def stdout_writer():
        try:
            async with write_stream_reader:
                async for session_message in write_stream_reader:
                    json = session_message.message.model_dump_json(by_alias=True, exclude_none=True)
                    data = (json + "\n").encode("utf-8")
                    view = memoryview(data)
                    while view:
                        await anyio.wait_writable(stdout_fd)
                        try:
                            written = os.write(stdout_fd, view)
                        except BlockingIOError:  # pragma: no cover
                            continue
                        view = view[written:]
        except (anyio.ClosedResourceError, BrokenPipeError, OSError):  # pragma: no cover
            await anyio.lowlevel.checkpoint()

    async with anyio.create_task_group() as tg:
        tg.start_soon(stdin_reader)
        tg.start_soon(stdout_writer)
        try:
            yield read_stream, write_stream
        finally:
            tg.cancel_scope.cancel()
            pending_line = ""
