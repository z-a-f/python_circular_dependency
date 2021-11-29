# Case Study 3: Implicit Dependency on `__init__.py`

## Problem

Before describing the problem, let us describe the files that are involved.

Consider a package structure that looks like this:

```shell
.
├── mypkg
│   ├── __init__.py
│   ├── bar
│   │   ├── __init__.py
│   │   └── fred.py
│   └── foo
│       ├── __init__.py
│       ├── baz.py
│       └── qux.py
└── main.py
```

<table>
<thead>
    <tr>
      <th><code>main.py</code></th>
      <th><code>mypkg/foo/__init__.py</code></th>
      <th><code>mypkg/bar/__init__.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> mypkg.bar.fred <span class="hljs-keyword">import</span> Fred
      <span></span>
f = Fred()
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> .baz <span class="hljs-keyword">import</span> Baz
<span class="hljs-keyword">from</span> .qux <span class="hljs-keyword">import</span> Qux
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> .fred <span class="hljs-keyword">import</span> Fred
</code></pre>
      </td>
    </tr>
  </tbody>
<!-------------------------------------------------------------------------->
  <thead>
    <tr>
      <th><code>mypkg/foo/baz.py</code></th>
      <th><code>mypkg/foo/qux.py</code></th>
      <th><code>mypkg/bar/fred.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> ..bar.fred <span class="hljs-keyword">import</span> Fred
      <span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Baz</span>:</span>
  <span class="hljs-keyword">pass</span>
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Qux</span>:</span>
  <span class="hljs-keyword">pass</span>
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> ..foo.qux <span class="hljs-keyword">import</span> Qux
      <span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Fred</span>:</span>
  <span class="hljs-keyword">pass</span>
</code></pre>
      </td>
    </tr>
  </tbody>
</table>

Notice, that there is no explicit cyclic dependency in this example:

```
main.py ───> mypkg/bar/fred.py ───> mypkg/foo/qux.py
```

In practice, however, the dependency is implied due to the `__init__.py` imports.
When you include imports inside the `__init__.py`, similar to the example above, you implicitly creating dependency of all the packages covered by that `__init__` on it.
That means, that in the example above, `mypkg/foo/qux.py` depends on the `mypkg/foo/baz.py` (because it is included in the `__init__.py`).

Calling the main file:

```shell
Traceback (most recent call last):
  File "./main.py", line 1, in <module>
    from mypkg.bar.fred import Fred
  File "./mypkg/bar/__init__.py", line 1, in <module>
    from .fred import Fred
  File "./mypkg/bar/fred.py", line 1, in <module>
    from ..foo.qux import Qux
  File "./mypkg/foo/__init__.py", line 1, in <module>
    from .baz import Baz
  File "./mypkg/foo/baz.py", line 1, in <module>
    from ..bar.fred import Fred
ImportError: cannot import name 'Fred' from partially initialized module 'mypkg.bar.fred' (most likely due to a circular import) (./mypkg/bar/fred.py)
```

## Solutions

### 1. Blank out the `__init__`'s

* (good) Simplest solution, suitable for libraries that hold a lot of "standalone" utilities
* (bad) Forces the clients to use the "long" fully qualified names

This is the simplest solution: just remove everything from all the `__init__.py` files, and use fully qualified names for all the member uses.
Unfortunately, this might not be the best option, especially for very deep projects.


<table>
<thead>
    <tr>
      <th><code>main.py</code></th>
      <th><code>mypkg/foo/__init__.py</code></th>
      <th><code>mypkg/bar/__init__.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> mypkg.bar.fred <span class="hljs-keyword">import</span> Fred
      <span></span>
f = Fred()
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"></code></pre>
      </td>
      <td>
      <pre><code class="language-python"></code></pre>
      </td>
    </tr>
  </tbody>
<!-------------------------------------------------------------------------->
  <thead>
    <tr>
      <th><code>mypkg/foo/baz.py</code></th>
      <th><code>mypkg/foo/qux.py</code></th>
      <th><code>mypkg/bar/fred.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> ..bar.fred <span class="hljs-keyword">import</span> Fred
      <span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Baz</span>:</span>
  <span class="hljs-keyword">pass</span>
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Qux</span>:</span>
  <span class="hljs-keyword">pass</span>
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> ..foo.qux <span class="hljs-keyword">import</span> Qux
      <span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Fred</span>:</span>
  <span class="hljs-keyword">pass</span>
</code></pre>
      </td>
    </tr>
  </tbody>
</table>

### 2. Use "interface" subpackage

*Note: the name "interface package/module" is not an official name, and was likely coined by James Murphy*

- (good) Clean, pythonic solution
- (good) if using very complex, very large project with a lot of dependencies
- (bad) Access to "subpackage-style" API becomes unavailable, obfuscated, or just long and hard.
- (bad) Requires refactoring of the existing projects

This solution makes sure there is no direct dependency of the subpackage members on the `package/__init__.py`.
To do that you use the [solution 1](#1) above for the main portions of the code, and introduce an "interface" that a client user interacts with.
Often times you might want to make the "interface" subpackage have a "user-friendly" name, while the real subpackages have `_` in the front.

The new structure of the project looks like the following

```shell
.
├── mypkg
|   ├── __init__.py
|   ├── _bar
|   |   ├── __init__.py
|   |   └── fred.py
|   ├── bar
|   |   └── __init__.py
|   ├── _foo
|   |   ├── __init__.py
|   |   ├── baz.py
|   |   └── qux.py
|   └── foo
|       └── __init__.py
└── main.py
```

The contents of the files will change accordingly

<table>
<thead>
    <tr>
      <th><code>main.py</code></th>
      <th><code>mypkg/foo/__init__.py</code></th>
      <th><code>mypkg/bar/__init__.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> mypkg.bar <span class="hljs-keyword">import</span> Fred
      <span></span>
f = Fred()
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> .._foo.baz <span class="hljs-keyword">import</span> Baz
<span class="hljs-keyword">from</span> .._foo..qux <span class="hljs-keyword">import</span> Qux
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> .._bar.fred <span class="hljs-keyword">import</span> Fred
</code></pre>
      </td>
    </tr>
  </tbody>
<!-------------------------------------------------------------------------->
<thead>
    <tr>
      <th></th>
      <th><code>mypkg/_foo/__init__.py</code></th>
      <th><code>mypkg/_bar/__init__.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td></td>
      <td>
      <pre><code class="language-python"></code></pre>
      </td>
      <td>
      <pre><code class="language-python"></code></pre>
      </td>
    </tr>
  </tbody>
<!-------------------------------------------------------------------------->
  <thead>
    <tr>
      <th><code>mypkg/_foo/baz.py</code></th>
      <th><code>mypkg/_foo/qux.py</code></th>
      <th><code>mypkg/_bar/fred.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> .._bar.fred <span class="hljs-keyword">import</span> Fred
      <span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Baz</span>:</span>
  <span class="hljs-keyword">pass</span>
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Qux</span>:</span>
  <span class="hljs-keyword">pass</span>
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> .._foo.qux <span class="hljs-keyword">import</span> Qux
      <span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Fred</span>:</span>
  <span class="hljs-keyword">pass</span>
</code></pre>
      </td>
    </tr>
  </tbody>
</table>
