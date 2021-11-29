# Case Study 1: Function Cross-Import

## Problem

This circular dependency happens when there are multiple files that try to import each other.

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
<span class="hljs-keyword">from</span> bar <span class="hljs-keyword">import</span> bar1, bar2
        <span></span>
f = foo1()
b1 = bar1()
b2 = bar2()
</code></pre>
      </td>
      <td>
        <pre><code class="language-python"><span class="hljs-keyword">from</span> bar <span class="hljs-keyword">import</span> bar1
        <span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;b = bar1()
&nbsp;&nbsp;...</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> foo <span class="hljs-keyword">import</span> foo1
      <span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;f = foo1()
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
    from bar import bar1
  File "./bar.py", line 1, in <module>
    from foo import foo1
ImportError: cannot import name 'foo1' from partially initialized module 'foo' (most likely due to a circular import) (./foo.py)
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

### 1. Move imports inside the calling functions

* (good) if `foo1` is the only function that calls `bar1` in the whole project.
* (good) if `foo1` is not called very often, and is the only fucntion in the `foo.py` that uses the `bar1`
* (bad) if a lot of different functions in the `foo.py` use the `bar` function

Because the functions are only needed once other functions are called, we can move the imports inside the functions themself.

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
        <pre><code class="language-python"><span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;<span class="hljs-keyword">from</span> bar <span class="hljs-keyword">import</span> bar1
&nbsp;&nbsp;b = bar1()
&nbsp;&nbsp;...</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;<span class="hljs-keyword">from</span> foo <span class="hljs-keyword">import</span> foo1
&nbsp;&nbsp;f = foo1()
&nbsp;&nbsp;...
</code></pre>
      </td>
    </tr>
  </tbody>
</table>

**Note:** You don't have to move the imports in both `foo.py` and `bar.py`.
As long as the cycle is broken, the problem is resolved.

### 2. Import packages/modules/files instead of functions

* (good) if there are a lot of files using the files from another file and vice versa
* (bad) if there are a lot of subfolders -- causes long call-names

Instead of letting python resolve the contents of the files, you can import the whole file without diving inside of its contents.

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
        <pre><code class="language-python"><span class="hljs-keyword">import</span> bar
        <span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;b = bar.bar1()
&nbsp;&nbsp;...</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">import</span> foo
      <span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;f = foo.foo1()
&nbsp;&nbsp;...
</code></pre>
      </td>
    </tr>
  </tbody>
</table>

*Note: This solution might be confusing, as there is a seemingly cycling dependency. However, this is not the case due to the way python's [import mechanics](https://docs.python.org/3/reference/import.html).*

### 3. Merge the files

If it looks like the files are using each other's functions a lot, it would make sense to just merge the files.

* (good) if the files are small
* (good) if the files really belong to the same subproject
* (bad) if the files are large or have to be separated

<table>
  <thead>
    <tr>
      <th><code>main.py</code></th>
      <th><code>foo.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td >
        <pre><code class="language-python"><span class="hljs-keyword">from</span> foo <span class="hljs-keyword">import</span> foo1
<span class="hljs-keyword">from</span> foo <span class="hljs-keyword">import</span> bar1, bar2
        <span></span>
f = foo1()
b1 = bar1()
b2 = bar2()
</code></pre>
      </td>
      <td>
        <pre><code class="language-python"><span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;b = bar1()
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;f = foo1()
&nbsp;&nbsp;...</code></pre>
      </td>
    </tr>
  </tbody>
</table>
