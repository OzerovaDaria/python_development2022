#!/usr/bin/python3
from sys import argv
from zlib import decompress
from os import path
import os

GIT_PATH = '../../.git'
OBJ_PATH = path.join(GIT_PATH, 'objects')
BRH_PATH = path.join(GIT_PATH, 'refs/heads')
IGNORE_OBJS = ['pack', 'info']

def createObjPath(obj):
    return path.join(OBJ_PATH, obj[:2], obj[2:])

def prepareObj(file):
    with open(file, 'rb') as f:
        fullobj = decompress(f.read())
        header, _, body = fullobj.partition(b'\x00')
        kind, size = header.split()
    return ( kind.decode(), int(size), body )

def checkType(expectedType, givenType):
    if expectedType != givenType:
        raise TypeError(f'File was expected to have kind "{expectedType}", instead "{givenType}"')

def parseCommit(file):
    kind, size, body = prepareObj(file)
    checkType('commit', kind)

    res = { 'tree': None, 'parent': None, 'author': None, 'commiter': None, 'msg': None }
    res['id'] = ''.join(file.split('/')[-2:])

    rawIt = iter(body.decode().split('\n'))
    while rawIt:
        line = next(rawIt)
        if not line:
            res['msg'] = '\n'.join(list(rawIt))
            break
        obj = line.split(' ', 1)
        res[obj[0]] = obj[1]

    return res

def getTreeRef(file):
    kind, size, body = prepareObj(file)
    checkType('tree', kind)
    return body.partition(b'\x00')[2][:20].hex()

def bodyParser(body, kind):
    if kind == 'commit':
        return body.decode()
    if kind == 'tree':
        res = []
        while body:
            treehdr, _, tail = body.partition(b'\x00')
            gitid, body = tail[:20], tail[20:]
            res.append(f'\t{treehdr.decode()} hex:{gitid.hex()}')
        return '\n'.join(res)
    return False

def printObj(file, prefix='', suffix=''):
    kind, size, body = prepareObj(file)
    print(prefix, 'kind: ', kind, suffix, sep='')
    print(prefix, 'size: ', size, suffix, sep='')
    if (pbody := bodyParser(body, kind)):
        for line in pbody.split('\n'):
            print(prefix, line, suffix, sep='')

def printTree(treePath, indent='  |'):
    try:
        while True:
            printObj(treePath, indent)
            treeRef = getTreeRef(treePath)
            treePath = createObjPath(treeRef)
            print(indent, '-'*10, sep='')
    except TypeError:
        pass

def printCommit(commit, prefix=''):
    print(prefix, commit['id'], sep='')
    printObj(createObjPath(commit['id']))
    print('-'*10)

def printAllObjects():
    for obj in os.listdir(OBJ_PATH):
        if obj in IGNORE_OBJS: continue
        objName = os.listdir(path.join(OBJ_PATH, obj))[0]
        objPath = path.join(OBJ_PATH, obj, objName)

        print(f'Object {path.join(obj, objName)}:')
        printObj(objPath)
        print('-'*10, '\n')


############# MAIN #############
argc = len(argv)

if argc == 1:
    print('Locally available branches:')
    for branch in os.listdir(BRH_PATH):
        print(branch)
else:
    if argv[1] == '--show':
        printAllObjects()
        exit()

    with open(path.join(BRH_PATH, argv[1]), 'r') as f:
        lastCommit = f.readline()[:-1] #to remove \n in the end
    commit = parseCommit(createObjPath(lastCommit))

    printCommit(commit, f'Last commit on branch {argv[1]}: ')
    print('Last commit\'s tree:', commit['tree'])
    printTree(createObjPath(commit['tree']))
    print('---End of the tree---\n\n')

    i = 0
    while commit['parent'] != None:
        commit = parseCommit(createObjPath(commit['parent']))
        i += 1

        printCommit(commit, f'Commit on HEAD^{i}: ')
        print('Tree of this commit:', commit['tree'])
        printTree(createObjPath(commit['tree']))
        print('---End of the tree---\n\n')

    print('+--- No more commit history on this branch ---+')
