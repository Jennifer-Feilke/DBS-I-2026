from contextlib import contextmanager


@contextmanager
def yield_tutorial():

    try:
        print("Hello")
        yield 1
    finally:
        print("Goodbye")


with yield_tutorial() as number:
    print(f"'{number}' was yielded")
