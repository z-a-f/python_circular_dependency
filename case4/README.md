# Case Study 4: Mixing Library and Script Code

## Problem

When mixing the library and script code or declaring a lot of global variables that are derived from some functions, it is easy to get into a big architectural issue.
Unfortunately, the only *good* solution for that problem is to complete change of the code structure and architecture.

Consider an example

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
foo1()
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> bar <span class="hljs-keyword">import</span> bar1, bar2
<span></span>
b1_global = bar1()
b2_global = bar2()
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> foo <span class="hljs-keyword">import</span> foo1, foo2
<span></span>
f1_global = foo1()
f2_global = foo2()
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
</code></pre>
      </td>
    </tr>
  </tbody>
</table>

The example shows that it is not clear how to resolve the circular dependency, as all the issues happen at import time.

## Solutions

Unfortunately, there are no good solutions for this problem, and it requires rewrite of the code architecture.

### X. (Non-Solution) Import packages instead of the functions from those packages

This trick doesn't work :/

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
foo1()
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">import</span> bar
<span></span>
b1_global = bar.bar1()
b2_global = bar.bar2()
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">import</span> foo
<span></span>
f1_global = foo.foo1()
f2_global = foo.foo2()
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
</code></pre>
      </td>
    </tr>
  </tbody>
</table>

### 1. Merge the files that are causing the circular dependency

Although no always possible, if you absolutely have to mix the library and script code, you can merge the files that cause the circular dependency.

<table>
<thead>
    <tr>
      <th><code>main.py</code></th>
      <th><code>foo.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr style="vertical-align:top">
      <td>
      <pre><code class="language-python"><span class="hljs-keyword">from</span> foo <span class="hljs-keyword">import</span> foo1
      <span></span>
foo1()
</code></pre>
      </td>
      <td>
      <pre><code class="language-python"><span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">foo2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar1</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
<span class="hljs-function"><span class="hljs-keyword">def</span> <span class="hljs-title">bar2</span><span class="hljs-params">()</span>:</span>
&nbsp;&nbsp;...
<span></span>
f1_global = foo1()
f2_global = foo2()
b1_global = bar1()
b2_global = bar2()
</code></pre>
      </td>
    </tr>
  </tbody>
</table>

