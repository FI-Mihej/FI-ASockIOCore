Welcome to the FI-ASockIOCore wiki!

# FI-ASockIOCore
FI Async Socket IO Core

##Strengths

* Async.
* Robust, fast and simple to use.
* _Named clients/services_ and anonymous clients. You can register client by name (keyword) and start working with it when it will be connected (through any of handled passive sockets).
* Secure. You _can restrict Named Clients connection_ by rules. For example you may allow Named Client with UNIX socket connection or from localhost and disallow from outside of the server or local network, etc.
* Can work with both messages and raw traffic. _Message length is almost unlimited (2^64 bytes)_.
* Has two types of API: 
    * By using server methods from a plane code. Slightly faster on small data chunks (up to few KiB) and on super big data chunks (5MiB and bigger). Gives full flexibility to the developer.
    * Class inheritance (like in asyncio). It is always faster on mid (few KiB and bigger) data chunks (in every implementation: asyncio, FI-ASockIOCore, etc.) because of CPU cache work. But it's not so flexible.
* Supports _sharing single server port_ between multiple server process instances (Linux (with kernel 3.9+) and Android, BSD, iOS, Windows).
* Works _with several passive sockets at the same time_. For example you can open few different TCP/UDP ports, few UNIX sockets and accept clients from all of them transparently.
* It can act as _both a server and a client_.
* Cross-platform
* Supports Python 3.2+ (in a few cases it is 3.3+).
    * Supports last PyPy Night Build (which implements Python 3.3)

## Short Examples

### Sending messages using server methods from the plane code

Message creation using marshal (much faster than pickle):

    data = ['some small or big string or other object', 1234, b'some bytes data', {1, 2, 3, 4}]
    command = ('do some work', data)
    compact_command = marshal.dumps(command)

Send single message:

    server.send_message_to_client(manager_client_id, compact_command)

Send list of 1000000 messages (you can use iterable for memory saving):

    server.send_messages_to_client(manager_client_id, [b'some data' for index in range(10**6)])

Run another IO iteration:

    io_iteration_result = server.io_iteration(io_iteration_timeout)

Where io io_iteration_result an object of class IoIterationResult:

    class IoIterationResult:
        def __init__(self):
            self.newly_connected_expected_clients = set()
            self.newly_connected_unknown_clients = set()
            self.clients_with_disconnected_connection = set()
            self.clients_have_data_to_read = set()
            self.clients_with_empty_output_fifo = set()

### Sending messages using class inheritance:

    class SimpleInlineProcessor(InlineProcessor):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
    
        def on__data_received(self, data: bytes):
            if b'close' == data:
                self.mark__socket_as_ready_to_be_closed(True)
            else:
                data += b'1234'
                self.output_messages.append(data)  # Send data back to client
    
        def on__output_buffers_are_empty(self):
            self.output_messages.append('I don\'t here you!')  # Send some data to client
    
        def on__connection_lost(self):
            print('Client with name "{}" is disconnected'.format(self.keyword))

## Full Examples

Some server and client examples can be found in folder "Examples And Benchmarks". 

This examples are part of tests set for a different FI-ASockIOCore work modes. Most of them are not ready to be published yet: comments, prints, tracing code, profiling code, etc.

### Notice

You can start **multiple instances** of the HTTP servers. They will share single port automatically on: Linux (with kernel 3.9+) and Android, BSD, iOS, Windows. 

_Sharing of sinple port is not as fast as using several independent ports for different processes_, but it is simple to use. So for a fair test it is better to start each server instance on a different port and run one independent benchmark instance per an each server instance.

## Benchmarks

### Benchmark results as a whole.

Machine: 
* Intel(R) Xeon(R) CPU E3-1246 v3 @ 3.50GHz
* 32 GB DDR3 RAM

OS:
* Ubuntu 14.04.4 LTS x86_64

#### Concurency tests (relative performance per concurent connections from 1 and up to 1000):

FI-ASockIOCore is an equivalent to asyncio, uvloop, golang, etc.

#### Message size tests - generate and send string with requested size to client (for 200 concurent connections)

FI-ASockIOCore - all tests passed in every mode. Unlike asyncio and especially Golang...

If FI-ASockIOCore with InlineProcessor == **1.0**, then:
* asyncio == **0.95** on up to few Kib; **1.18** on 32 KiB - 700Kib; **0.95** on 700 Kib; **0.5** on 7+ MiB
    * **But**:
        * it **can't** pass test when string size == 8760000 bytes (and sometimes on other big string sizes): wrk always returns "0.0R/s; 2.41MiB/s"
* FI-ASockIOCore with server methods API == **1.0** on up to few KiB; **0.64** on 1MiB; and **1.0** on 5+ MiB
* TornadoWeb == about **0.5** (with small and midle string) - **0.75** (512+ KiB) (didn't test yet with the last set of benchmark tests so this is not precise)
* GoLang simple http server from vmbench project == about **1.7** - **2.2**
    * **But**: 
        * you **can't** restrict GoLang to really use only one CPU core (even with GOMAXPROCS=1); 
        * it (GoLang) **crashes** (especially when GOMAXPROCS > 1). Randomly and often. And as far as I know, it's a bug in a GoLang core (yet not fixed in the 1.6.2 release).

### Benchmark results in detail.

Results of last tests can be found in folder 'Examples And Benchmarks/BENCHMARK RESULTS'. In separate json files.

### Run your own benchmarks

To run HTTP benchmarks you need to have https://github.com/wg/wrk unpacked to some folder

Also you need to have https://github.com/MagicStack/vmbench unpacked to some folder. **But it has few critical bugs** (including division by zero, etc.) and my pull request can be still in the list **so it is better to use fixed version from my fork**: https://github.com/FI-Mihej/vmbench


1. Set path to 'vmbench' in "./Examples And Benchmarks/HTTP over Raw Connection/BENCHMARKING CLIENT/http_client_set_of_tests.py" (top of the file)
2. Set path to 'wrk' in 'your_path_to_vmbench-master/http_client' (search for "wrk" word in the code)

## Development

### Todo list:
1. Complete the process of refactoring.
2. Integrate improved message reading algorithm (will be some faster).
3. Add proper UDP support.
4. Add SSL/TLS support.
5. Add pipe support as a transport for Unix-like systems. (Maybe).

### Code notice:
* Code is in process of name refactoring. Inteface names are already changed, bun not local names. So code can be confusing to understand it properly if you want to read it.
* Code made to be fast and robust. So in some cases, ideal beauty may not be a priority. See an appropriate code comments.
