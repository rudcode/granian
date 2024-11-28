import asyncio


class AsyncTaskKeepReference:
    tasks = set()

    def __init__(self, func):
        self.async_func = func

    async def __call__(self, *args, **kwargs):
        task = asyncio.current_task()
        self.tasks.add(task)
        try:
            result = await self.async_func(*args, **kwargs)
        finally:
            self.tasks.remove(task)
        return result

def future_watcher_wrapper(inner):
    @AsyncTaskKeepReference
    async def future_watcher(watcher):
        try:
            await inner(watcher.scope, watcher.proto)
        except BaseException as exc:
            watcher.err(exc)
            return
        watcher.done()

    return future_watcher
