from utruecaller_api import search_phonenumber, get_access_tokens, _list
from concurrent.futures import ThreadPoolExecutor

MAX_WORKERS = 64

@_list
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def bulk_search(numbers: list[str]):
    with ThreadPoolExecutor(max_workers=64) as executor:
        return list(executor.map(lambda number, key: search_phonenumber(number, None, key), list(zip(divide_chunks(numbers, 5), get_access_tokens(input("Google Username: "), input("Google Password: "), (numbers.__len__()//5)+1)))))

if __name__ == "__main__":
    bulk_search(eval(input("Numbers(input a list): ")))