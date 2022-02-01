from talon import Module, actions
import asyncio
import struct
import logging
import json
import threading
from . import run_context

# logging.basicConfig(level=logging.DEBUG)

MAX_MESSAGE_SIZE = 10 * 1024 * 1024

mod = Module()

class Client:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.outbound_messages = asyncio.Queue()
    
    async def handle(self):
        await asyncio.gather(self._handle_send(), self._handle_recv())

    def send(self, type: str, contents: object):
        message = {
            "type": type,
            "contents": contents
        }

        self.outbound_messages.put_nowait(message)

    def _handle_message(self, message: str):
        print(message)
        message = json.loads(message)
        actions.user.rpc_handle_message(message["type"], message["contents"])

    async def _handle_send(self):
        while True:
            message = await self.outbound_messages.get()
            message = json.dumps(message)
            logging.info(f"Sending {message}")
            buffer = message.encode("utf8")
            buffer = struct.pack("I", len(buffer)) + buffer
            self.writer.write(buffer)
            logging.info("Sent!")

    async def _handle_recv(self):
        while True:
            message_size = await self.reader.read(4)
            if len(message_size) < 4:
                logging.warn("Client disconnected while reading message size.")
                break

            message_size = struct.unpack("I", message_size)[0]
            if message_size > MAX_MESSAGE_SIZE:
                logging.error(f"Client tried to send a message of {message_size} bytes, exceeding the maximum size of {MAX_MESSAGE_SIZE}.")
                break

            message = await self.reader.read(message_size)
            if len(message) < message_size:
                logging.warn("Client disconnected while reading message contents.")
                break

            try:
                message = message.decode("utf8")
            except UnicodeDecodeError:
                logging.error("Unable to decode client message")
                break
        
            logging.info("Dispatching message.")
            self._handle_message(message)

active_client = None

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):        
    global active_client
    client = Client(reader, writer)
    active_client = client
    await client.handle()
    
async def run_server():
    server = await asyncio.start_server(handle_client, "localhost", 31337)
    async with server:
        await server.serve_forever()

@mod.action_class
class RemoteActions:
    def rpc_handle_message(type: str, contents: object):
        """Receives a message from the active window"""
        logging.info(f"Received RPC message [{type}]: {contents}")

    def rpc_send_message(type: str, contents: object):
        """Sends a message to the active window"""
        global active_client
        if not active_client:
            logging.warn("No active client to send messages to!")
            return
        
        logging.info(f"Sending RPC message [{type}]: {contents}")
        active_client.send(type, contents)

class RunContext:
    def __init__(self):
        self.loop = asyncio.new_event_loop()

    def start(self):
        self.thread = threading.Thread(target=self._pump_loop)
        self.task = self.loop.create_task(run_server())
        self.thread.start()
    
    def stop(self):
        self.loop.call_soon_threadsafe(self.task.cancel)
        logging.info("Canceling RPC server task..")
        self.thread.join()
        logging.info("Ended previous RPC thread!")

    def _pump_loop(self):
        try:
            self.loop.run_until_complete(self.task)
        except asyncio.CancelledError:
            pass
        finally:
            logging.info("RPC thread finished running.")

if run_context.context:    
    run_context.context.stop()
    logging.info("Stopped previous RPC run context")
else:
    logging.info("No previous RPC run context to stop.")
    
run_context.context = RunContext()
run_context.context.start()
