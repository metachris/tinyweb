# https://github.com/metachris/tinyweb
_S='allowed_access_control_methods'
_R='
'
_Q=b'
'
_P='image/jpeg'
_O='GET'
_N='allowed_access_control_headers'
_M='allowed_access_control_origins'
_L='max_body_size'
_K='text/html'
_J='*'
_I=False
_H=b''
_G='application/json'
_F='save_headers'
_E=True
_D='methods'
_C='Content-Length'
_B='Content-Type'
_A=None
import uasyncio as asyncio,uasyncio.core,ujson as json,gc,uos as os,sys,json,uerrno as errno,usocket as socket
try:import logging;log=logging.getLogger('WEB');log_err=log.error;log_exc=log.exc
except ImportError:
	def log_err(msg):print('ERROR:WEB:%s'%msg)
	def log_exc(exc,msg):log_err(msg);sys.print_exception(exc)
IS_UASYNCIO_V3=hasattr(asyncio,'__version__')and asyncio.__version__>=(3,)
MIME_TYPES_PER_EXT={'.txt':'text/plain','.htm':_K,'.html':_K,'.css':'text/css','.csv':'text/csv','.js':'application/javascript','.xml':'application/xml','.xhtml':'application/xhtml+xml','.json':_G,'.zip':'application/zip','.pdf':'application/pdf','.ts':'application/typescript','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf','.otf':'font/otf','.jpg':_P,'.jpeg':_P,'.png':'image/png','.gif':'image/gif','.svg':'image/svg+xml','.ico':'image/x-icon'}
def urldecode_plus(s):
	D='%';s=s.replace('+',' ');C=s.split(D);B=C[0]
	for A in C[1:]:
		if len(A)>=2:B+=chr(int(A[:2],16))+A[2:]
		elif len(A)==0:B+=D
		else:B+=A
	return B
def parse_query_string(s):
	B={};C=s.split('&')
	for D in C:
		A=[urldecode_plus(A)for A in D.split('=',1)]
		if len(A)==1:B[A[0]]=''
		else:B[A[0]]=A[1]
	return B
class HTTPException(Exception):
	def __init__(A,code=400):A.code=code
class request:
	def __init__(A,_reader):A.reader=_reader;A.headers={};A.method=_H;A.path=_H;A.query_string=_H
	async def read_request_line(A):
		while _E:
			B=await A.reader.readline()
			if B==_Q or B==b'
':continue
			break
		C=B.split()
		if len(C)!=3:raise HTTPException(400)
		A.method=C[0];D=C[1].split(b'?',1);A.path=D[0]
		if len(D)>1:A.query_string=D[1]
	async def read_headers(B,save_headers=[]):
		while _E:
			gc.collect();C=await B.reader.readline()
			if C==_Q:break
			A=C.split(b':',1)
			if len(A)!=2:raise HTTPException(400)
			if A[0]in save_headers:B.headers[A[0]]=A[1].strip()
	async def read_parse_form_data(A):
		F=b'Content-Type';E=b'Content-Length';gc.collect()
		if E not in A.headers:return{}
		if F not in A.headers:return{}
		B=int(A.headers[E])
		if B>A.params[_L]or B<0:raise HTTPException(413)
		C=await A.reader.readexactly(B);D=A.headers[F].split(b';',1)[0]
		try:
			if D==b'application/json':return json.loads(C)
			elif D==b'application/x-www-form-urlencoded':return parse_query_string(C.decode())
		except ValueError:raise HTTPException(400)
class response:
	def __init__(A,_writer):B=_writer;A.writer=B;A.send=B.awrite;A.code=200;A.version='1.0';A.headers={}
	async def _send_headers(A):
		B='HTTP/{} {} MSG
'.format(A.version,A.code)
		for (C,D) in A.headers.items():B+='{}: {}
'.format(C,D)
		B+=_R;gc.collect();await A.send(B)
	async def error(A,code,msg=_A):
		B=msg;A.code=code
		if B:A.add_header(_C,len(B))
		await A._send_headers()
		if B:await A.send(B)
	async def redirect(A,location,msg=_A):
		B=msg;A.code=302;A.add_header('Location',location)
		if B:A.add_header(_C,len(B))
		await A._send_headers()
		if B:await A.send(B)
	def add_header(A,key,value):A.headers[key]=value
	def add_access_control_headers(A):A.add_header('Access-Control-Allow-Origin',A.params[_M]);A.add_header('Access-Control-Allow-Methods',A.params[_S]);A.add_header('Access-Control-Allow-Headers',A.params[_N])
	async def start_html(A):A.add_header(_B,_K);await A._send_headers()
	async def html(A,content):await A.start_html();await A.send(content)
	async def json(A,body):A.add_header(_B,_G);await A._send_headers();await A.send(json.dumps(body))
	async def send_file(A,filename,content_type=_A,content_encoding=_A,max_age=2592000):
		L='.';D=content_encoding;C=content_type;B=filename
		try:
			H=os.stat(B);I=str(H[6]);A.add_header(_C,I)
			if C:A.add_header(_B,C)
			else:
				E=L+B.split(L)[-1]
				if E in MIME_TYPES_PER_EXT:A.add_header(_B,MIME_TYPES_PER_EXT[E])
			if D:A.add_header('Content-Encoding',D)
			A.add_header('Cache-Control','max-age={}, public'.format(max_age))
			with open(B)as J:
				await A._send_headers();gc.collect();F=bytearray(128)
				while _E:
					G=J.readinto(F)
					if G==0:break
					await A.send(F,sz=G)
		except OSError as K:
			if K.args[0]in(errno.ENOENT,errno.EACCES):raise HTTPException(404)
			else:raise
async def restful_resource_handler(req,resp,param=_A):
	F=param;C=req;A=resp;D=await C.read_parse_form_data()
	if C.query_string!=_H:D.update(parse_query_string(C.query_string.decode()))
	G,H=C.params['_callmap'][C.method];gc.collect()
	if F:B=G(D,F,**H)
	else:B=G(D,**H)
	gc.collect()
	if isinstance(B,asyncio.type_gen):
		A.version='1.1';A.add_header('Connection','close');A.add_header(_B,_G);A.add_header('Transfer-Encoding','chunked');A.add_access_control_headers();await A._send_headers()
		for I in B:J=len(I.encode('utf-8'));await A.send('{:x}
'.format(J));await A.send(I);await A.send(_R);gc.collect()
		await A.send('0

')
	else:
		if type(B)==tuple:A.code=B[1];B=B[0]
		elif B is _A:raise Exception('Result expected')
		if type(B)is dict:E=json.dumps(B)
		else:E=B
		A.add_header(_B,_G);A.add_header(_C,str(len(E)));A.add_access_control_headers();await A._send_headers();await A.send(E)
class webserver:
	def __init__(A,request_timeout=3,max_concurrency=3,backlog=16,debug=_I):A.loop=asyncio.get_event_loop();A.request_timeout=request_timeout;A.max_concurrency=max_concurrency;A.backlog=backlog;A.debug=debug;A.explicit_url_map={};A.catch_all_handler=_A;A.parameterized_url_map={};A.conns={};A.processed_connections=0
	def _find_url_handler(A,req):
		B=req
		if B.path in A.explicit_url_map:return A.explicit_url_map[B.path]
		D=B.path.rfind(b'/')+1;C=B.path[:D]
		if len(C)>0 and C in A.parameterized_url_map:B._param=B.path[D:].decode();return A.parameterized_url_map[C]
		if A.catch_all_handler:return A.catch_all_handler
		return _A,_A
	async def _handle_request(B,req,resp):
		A=req;await A.read_request_line();A.handler,A.params=B._find_url_handler(A)
		if not A.handler:await A.read_headers();raise HTTPException(404)
		resp.params=A.params;await A.read_headers(A.params[_F])
	async def _handler(D,reader,writer):
		E=writer;gc.collect()
		try:
			A=request(reader);C=response(E);await asyncio.wait_for(D._handle_request(A,C),D.request_timeout)
			if A.method==b'OPTIONS':C.add_access_control_headers();C.add_header(_C,'0');await C._send_headers();return
			if A.method not in A.params[_D]:raise HTTPException(405)
			gc.collect()
			if hasattr(A,'_param'):await A.handler(A,C,A._param)
			else:await A.handler(A,C)
		except (asyncio.CancelledError,asyncio.TimeoutError):pass
		except OSError as B:
			if B.args[0]not in(errno.ECONNABORTED,errno.ECONNRESET,32):
				try:await C.error(500)
				except Exception as B:log_exc(B,'')
		except HTTPException as B:
			try:await C.error(B.code)
			except Exception as B:log_exc(B)
		except Exception as B:
			log_err(A.path.decode());log_exc(B,'')
			try:
				await C.error(500)
				if D.debug:sys.print_exception(B,C.writer.s)
			except Exception as B:pass
		finally:
			await E.aclose()
			if len(D.conns)==D.max_concurrency:D.loop.create_task(D._server_coro)
			del D.conns[id(E.s)]
	def add_route(C,url,f,**F):
		H='URL exists';B=url
		if B==''or'?'in B:raise ValueError('Invalid URL')
		A={_D:[_O],_F:[],_L:1024,_N:_J,_M:_J};A.update(F);A[_S]=', '.join(A[_D]);A[_D]=[B.encode()for B in A[_D]];A[_F]=[B.encode()for B in A[_F]]
		if B.endswith('>'):
			D=B.rfind('<');E=B[:D];D+=1;G=B[D:-1]
			if E.encode()in C.parameterized_url_map:raise ValueError(H)
			A['_param_name']=G;C.parameterized_url_map[E.encode()]=f,A
		if B.encode()in C.explicit_url_map:raise ValueError(H)
		C.explicit_url_map[B.encode()]=f,A
	def add_resource(F,cls,url,**G):
		C=[];D={}
		try:A=cls()
		except TypeError:A=cls
		for B in [_O,'POST','PUT','PATCH','DELETE']:
			E=B.lower()
			if hasattr(A,E):C.append(B);D[B.encode()]=getattr(A,E),G
		F.add_route(url,restful_resource_handler,methods=C,save_headers=[_C,_B],_callmap=D)
	def catchall(A):
		B={_D:[b'GET'],_F:[],_L:1024,_N:_J,_M:_J}
		def C(f):A.catch_all_handler=f,B;return f
		return C
	def route(A,url,**B):
		def C(f):A.add_route(url,f,**B);return f
		return C
	def resource(B,url,method=_O,**C):
		A=method
		def D(f):B.add_route(url,restful_resource_handler,methods=[A],save_headers=[_C,_B],_callmap={A.encode():(f,C)});return f
		return D
	async def _tcp_server(B,host,port,backlog):
		E=socket.getaddrinfo(host,port,0,socket.SOCK_STREAM)[0][-1];A=socket.socket(socket.AF_INET,socket.SOCK_STREAM);A.setblocking(_I);A.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);A.bind(E);A.listen(backlog)
		try:
			while _E:
				if IS_UASYNCIO_V3:yield uasyncio.core._io_queue.queue_read(A)
				else:yield asyncio.IORead(A)
				C,G=A.accept();C.setblocking(_I);B.processed_connections+=1;F=id(C);D=B._handler(asyncio.StreamReader(C),asyncio.StreamWriter(C,{}));B.conns[F]=D;B.loop.create_task(D)
				if len(B.conns)==B.max_concurrency:yield _I
		except asyncio.CancelledError:return
		finally:A.close()
	def run(A,host='127.0.0.1',port=8081,loop_forever=_E):
		A._server_coro=A._tcp_server(host,port,A.backlog);A.loop.create_task(A._server_coro)
		if loop_forever:A.loop.run_forever()
	def shutdown(A):
		asyncio.cancel(A._server_coro)
		for (C,B) in A.conns.items():asyncio.cancel(B)
