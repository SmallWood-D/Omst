import subprocess
import time
import os.path as path
import asyncio

from pymongo import MongoClient

mongoClient = MongoClient("mongodb://localhost:27017/?retryWrites=true&w=majority")


async def write_result(test_name, result):
    db = mongoClient.results
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    db.reviews.insert_one({"name": test_name, "result": result, "lut": current_time})


async def run_test(test_name):
    output = subprocess.run([path.join(".", "resources", "tester.bat"), test_name], capture_output=True)
    return output.stdout.decode('ascii')


def print_all_results():
    db = mongoClient.results
    all_results = db.reviews.find({})
    for e in all_results:
        print(e)


async def run_tests():
    out = await run_test("hello")
    await write_result("hello", out)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_tests())
loop.close()

print_all_results()

