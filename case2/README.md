# Case Study 2: Type Annotations

## Problem

Similar to the [case 1](../case1), this circular dependency happens because of cross-usage of resources in different files.
However, the difference is that **types are not evaluated at runtime**.
Types are compile-time or static-analysis-time constructs.
That's the solutions are slightly different.

For example, suppose you have three files in your working directory as described below

<table>
  <thead>
    <tr>
      <th><code>main.py</code></th>
      <th><code>foo.py</code></th>
      <th><code>bar.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
        <pre><code class="language-python"><span class="hljs-keyword">from</span> foo <span class="hljs-keyword">import</span> foo1
        <span></span>
f = foo1()
</code></pre>
      </td>
      <td>
        <pre><code class="language-python"><span class="hljs-keyword">from</span> bar <span class="hljs-keyword">import</span> Bar
        <span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Foo</span>:</span>
&nbsp;&nbsp;<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">__init__</span><span class="hljs-params">(self, b: Bar)</span>:</span>
&nbsp;&nbsp;&nbsp;&nbsp;self.b = b
    <span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;<span class="hljs-keyword">from</span> bar <span class="hljs-keyword">import</span> bar1
&nbsp;&nbsp;b: Bar = bar1()
&nbsp;&nbsp;...
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> foo <span class="hljs-keyword">import</span> Foo
<span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Bar</span>:</span>
&nbsp;&nbsp;<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">__init__</span><span class="hljs-params">(self, f: Foo)</span>:</span>
&nbsp;&nbsp;&nbsp;&nbsp;self.f = f
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span> -&gt; <span class="hljs-title">Bar</span>:</span>
&nbsp;&nbsp;...
</code></pre>
      </td>
    </tr>
  </tbody>
</table>

If you call the `main.py`, you will receive an error

```{shell .numberLines}
Traceback (most recent call last):
  File "./main.py", line 1, in <module>
    from foo import foo1
  File "./foo.py", line 1, in <module>
    from bar import Bar
  File "./bar.py", line 1, in <module>
    from foo import Foo
ImportError: cannot import name 'Foo' from partially initialized module 'foo' (most likely due to a circular import) (./foo.py)
```

The traceback above explains the reasoning quite well: `main.py` tries to import `foo.foo1`, but to do so it needs to import `bar.bar1`, which in turn tries to import `foo.foo1`.
Notice that the error is raised from the `foo.py` (not `bar.py`), and it states that `foo` is *partially initialized*.
That means that `foo.py` cannot be imported because it is already *in the process of importing*.

```
main.py ───> foo.py ───> bar.py
             ^               │
             └───────────────┘
```

## Solutions

Note that in this example there is no true "import time" dependency. The dependency in the example is purely "calltime", meaning the `foo.py` doesn't need access to the `bar.py` until the user decides to use the `foo1`.

### X. (Non-Solution) Use `__future__.annotations`

* (good) Resolves the cyclic dependency
* (bad) Breaks static analyzers

The `__future__.annotations` changes the way python handles the annotations.
Currently, it converts the annotations to strings, and does not require imports (py=3.8, future=0.18).
*Note: this behavior might change in the future (see PEP563, PEP649).*

<table>
  <thead>
    <tr>
      <th><code>foo.py</code></th>
      <th><code>bar.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
        <pre><code class="language-python"><span class="hljs-keyword">from</span> __future__ <span class="hljs-keyword">import</span> annotations
        <span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Foo</span>:</span>
&nbsp;&nbsp;<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">__init__</span><span class="hljs-params">(self, b: Bar)</span>:</span>
&nbsp;&nbsp;&nbsp;&nbsp;self.b = b
    <span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;<span class="hljs-keyword">from</span> bar <span class="hljs-keyword">import</span> bar1
&nbsp;&nbsp;b: Bar = bar1()
&nbsp;&nbsp;...
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> __future__ <span class="hljs-keyword">import</span> annotations
<span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Bar</span>:</span>
&nbsp;&nbsp;<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">__init__</span><span class="hljs-params">(self, f: Foo)</span>:</span>
&nbsp;&nbsp;&nbsp;&nbsp;self.f = f
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span> -&gt; <span class="hljs-title">Bar</span>:</span>
&nbsp;&nbsp;...
</code></pre>
      </td>
    </tr>
  </tbody>
</table>


However, this is **NOT A SOLUTION**.
One of the most common uses for the type annotations is static code analysis.
If you try running `mypy` on this "solution", you will get an error:

```shell
./bar.py:4: error: Name "Foo" is not defined
./foo.py:4: error: Name "Bar" is not defined
Found 2 errors in 2 files (checked 1 source file)
```

### 1. Use `__future__.annotations` + subpackage import

* (good) Resolves the cyclic dependency
* (bad) The types don't look good and long

This is the same solution as above + a resolution for the static analyzers.

<table>
  <thead>
    <tr>
      <th><code>foo.py</code></th>
      <th><code>bar.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
        <pre><code class="language-python"><span class="hljs-keyword">from</span> __future__ <span class="hljs-keyword">import</span> annotations
<span class="hljs-keyword">import</span> bar
        <span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Foo</span>:</span>
&nbsp;&nbsp;<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">__init__</span><span class="hljs-params">(self, b: bar.Bar)</span>:</span>
&nbsp;&nbsp;&nbsp;&nbsp;self.b = b
    <span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;b: bar.Bar = bar.bar1()
&nbsp;&nbsp;...
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> __future__ <span class="hljs-keyword">import</span> annotations
<span class="hljs-keyword">import</span> foo
<span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Bar</span>:</span>
&nbsp;&nbsp;<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">__init__</span><span class="hljs-params">(self, f: foo.Foo)</span>:</span>
&nbsp;&nbsp;&nbsp;&nbsp;self.f = f
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span> -&gt; <span class="hljs-title">Bar</span>:</span>
&nbsp;&nbsp;...
</code></pre>
      </td>
    </tr>
  </tbody>
</table>

### 2. Conditional imports

* (good) The type names are not too long
* (bad) Need to import future and annotations

This is (imho) the proper way of handling the type annotation imports.
Because python prodes you with a mechanism to check if the current run is part of type analysis, you should take advantage of it.

<table>
  <thead>
    <tr>
      <th><code>foo.py</code></th>
      <th><code>bar.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
        <pre><code class="language-python"><span class="hljs-keyword">from</span> __future__ <span class="hljs-keyword">import</span> annotations
<span class="hljs-keyword">from</span> typing <span class="hljs-keyword">import</span> TYPE_CHECKING
        <span></span>
<span class="hljs-keyword">if</span> TYPE_CHECKING:
&nbsp;&nbsp;<span class="hljs-keyword">from</span> bar <span class="hljs-keyword">import</span> Bar
<span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Foo</span>:</span>
&nbsp;&nbsp;<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">__init__</span><span class="hljs-params">(self, b: Bar)</span>:</span>
&nbsp;&nbsp;&nbsp;&nbsp;self.b = b
    <span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;<span class="hljs-keyword">from</span> bar <span class="hljs-keyword">import</span> bar1
&nbsp;&nbsp;b: Bar = bar1()
&nbsp;&nbsp;...
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> __future__ <span class="hljs-keyword">import</span> annotations
<span class="hljs-keyword">from</span> typing <span class="hljs-keyword">import</span> TYPE_CHECKING
<span></span>
<span class="hljs-keyword">if</span> TYPE_CHECKING:
&nbsp;&nbsp;<span class="hljs-keyword">from</span> foo <span class="hljs-keyword">import</span> Foo
<span></span>
<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">Bar</span>:</span>
&nbsp;&nbsp;<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">__init__</span><span class="hljs-params">(self, f: Foo)</span>:</span>
&nbsp;&nbsp;&nbsp;&nbsp;self.f = f
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span> -&gt; <span class="hljs-title">Bar</span>:</span>
&nbsp;&nbsp;...
</code></pre>
      </td>
    </tr>
  </tbody>
</table>
