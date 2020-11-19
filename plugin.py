import importlib
import os
# import lupa
#
# from lupa import LuaRuntime
# #
# with open('test.lua', 'r', encoding='utf-8') as f:
#     code = f.read()


# def initPlugin(payload):
#     lua = LuaRuntime(unpack_returned_tuples=True)
#     lua.execute(code)
#     g = lua.globals()
#     newPayload = g.channgePayload(payload)
#     return newPayload.encode()

def findAllPluginsName(path = '/Plugins'):
    for root, dirs, files in os.walk(os.path.dirname(__file__)+path):
        return files

if __name__ == '__main__':
    files = findAllPluginsName()
    print(files[0])
    module = importlib.import_module('.test1', 'Plugins')
    print(module.test())
