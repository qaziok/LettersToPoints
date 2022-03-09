def desmos(x,y):
    return f'({x},{-y})'


def xlib(x,y):
    return '{' + f'{x},{y}' + '}'


def gdi(x,y):
    return f'{x},{y}'


def directx(x,y):
    return '{'+f'XMFLOAT3({x}f,{y}f,{1.0}f),XMFLOAT3(0.0f,0.0f,1.0f)'+'},\n' \
           '{'+f' XMFLOAT3({x}f,{y}f,{-1.0}f),XMFLOAT3(0.0f,0.0f,-1.0f)'+'}'
