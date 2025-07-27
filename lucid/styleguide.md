# Visualization Pipeline Style Guide

This style guide outlines best practices and conventions for writing code that is easy to read, maintain, and collaborate on.

The purpose of this guide is to help ensure consistency and efficiency across our codebase, reduce the likelihood of bugs, and increase the speed of development. Keep this in mind, and know when to break the rules. If at any point deviating from these guidelines would make the most sense, do so.

This guide is a living document and will be updated over time as our coding standards and best practices evolve.

# General

* **Readability comes first**. Code is read more often than it is written. Write your code to be readable. Name your variables and methods to convey information. If a function is too long to parse, break it apart. Add comments to especially tricky bits.  
* **Do not pre-optimize, do not over-optimize**. Write readable code first. If performance becomes an issue, set *measurable* performance goals, and make the changes necessary to achieve those.  
* **Error handling**  
  * **Be specific when catching exceptions**. Do not use catch-alls.  
  * **Know when to let things break**. It is sometimes better to let a program break completely rather than introduce unintended behavior.  
  * **Errors are louder than warnings**. If something is critical for the user to know, use an error over a warning, e.g. deleting from a non-permitted directory.  
* **Docstrings**  
  * **Document your functions and classes with docstrings**. Add the information necessary to understand how to use the object. That can be a single line, or a full breakdown of arguments, return values, and examples. Documenting public methods is more important than documenting private methods.  
  * Use the [Google Python Style Guide format for docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).  
  * Module doc strings have the standard order of   
    * Module Name  
    * Module Description  
    * Notes  
* **Default values**  
  * **Only provide default argument values when there's a reason to**. A function that reads a file from a given path shouldn't have a default path value. Optional arguments must have default values.  
  * **Default values must be type-appropriate**. A default value for a list of strings should not be an empty string.  
* **Empty (or zero) values**  
  * **Use None instead of an empty value**. This greatly reduces the chance of code looking like it is working and creates uniform value verification across all projects.  
* **Dead code is bad code**. Unused code creates bloat and hurts readability. Remove dead code when creating pull requests to shared branches.  
* **Incorrect documentation is worse than no documentation**. When making changes to a documented piece of code, always update the documentation to reflect any changes.  
* **Tests** \- TBD  
* **Logging and debugging** \- TBD  
* **Indentations** \- Configure your IDE so tabs are processed as 4 spaces.

# Python

* We rely on **PEP 8 as a base style guide** for Python code. Additionally, PEP 257 describes good conventions for docstrings, and PEP 484 describes type hinting.  
  * [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)  
  * [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)  
  * [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)  
  * Anything written in this document takes precedence over the PEPs.  
* **Maintain compatibility with the lowest Python version** (3.9) in our toolchain.  
  * Notable missing features:  
    * [PEP 634: Structural Pattern Matching (3.10)](https://docs.python.org/3/whatsnew/3.10.html#pep-634-structural-pattern-matching)  
    * [PEP 604: New Type Union Operator (3.10)](https://docs.python.org/3/whatsnew/3.10.html#pep-604-new-type-union-operator)  
* **Do not add shebangs to the start of scripts**. A shebang (\#\!) at the start of an executable file tells a unix-based system what to use to execute the file. [Some Windows installations of Python handle specific hardcoded shebang commands](https://docs.python.org/3/using/windows.html#shebang-lines). We cannot rely on that being the case across all user machines. More importantly, we do not want to use a single global interpreter to run our projects. Each project should be invoked from the appropriate virtual environment.  
* **An important note regarding mutable arguments**: Python evaluates default parameters on function definition, not on function call. This means that mutable defaults (like lists or dicts) are shared between calls, and can lead to unexpected side effects. It is usually preferable to default these types to None and set the actual default inside the function body. See [this section in the Hitchhiker's Guide](https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments).  
* **import**   
  * Imports should be grouped in the following order:  
    * Standard library imports.  
    * Related third party imports.  
    * Local application/library specific imports.  
  * Put a blank line between each group of imports.  
  * Remove unused imports. Make sure no unused imports remain when creating pull requests to shared branches.  
  * When importing, try not to pollute the namespace.  
  * Never from x import \*. Always be explicit about your imports.  
  * Prefer from x import y over import x.y as z  
    * Exceptions may include common 3rd party api idioms  
    * If an import name must be done as something else to prevent namespace conflicts, make it clear, do not abbreviate.  
* **Blank Lines**  
  * Surround top-level function and class definitions with two blank lines.  
  * Method definitions inside a class are surrounded by a single blank line.  
  * Extra blank lines may be used to separate groups of related functions.  
  * Use blank lines in functions sparingly to indicate logical sections.  
  * Files should end with a single blank line. Trim extra whitespace at end of lines, and extra blank lines at end of files. Set up your IDE to handle this automatically.  
* **Naming conventions**  
  * As PEP8 suggests: snake\_case for variable names and functions, PascalCase for class names.  
  * Private methods should be denoted with an underscore beforehand (\_some\_private\_method()).  
  * Constants should use ALL CAPS.  
  * There are two acceptable ways of denoting module level privacy (see [stack overflow discussion](https://stackoverflow.com/questions/3602110/python-private-module-in-a-package)).  
    * Prefix the module name with a single leading underscore (e.g. \_foo.py)  
    * Create a submodule named “private” and nest the modules under it you wish to be private.  
  * Properties vs Returns  
    * Properties should simply be the exact property (object.property)  
    * Methods that return a value but are not a property should start with ‘get’ (object.get\_property()).  
    * Properties should be simple to compute, as they will always do so when called.  
* **Indentations**  
  * Indents should be 4 spaces  
* **Comments**  
  * Should be complete sentences.  
  * Should be grammatically correct.  
  * Use \>\>\> before a line of example code.  
* **Type hints**  
  * Always type hint your functions.  
  * Currently python 3.9.7 is the standard for DCCs and other software we currently use, therefore we do not have some of the newer features for type hinting in 3.10 and above.  
    * If your function returns multiple types, generally they should be Unioned.  
    * If an argument can be anything, import Any from Typing and use that rather than leaving it blank.  
* **Dunder names (\_\_xyz\_\_)**  
  * Do not create your own dunder/magic methods. These create unnecessary complexity and rarely create a large enough benefit to justify handling.  
* **String formatting (preferred)**  
  * Generally use f strings over format(), unless it explicitly adds to code clarity. Line lengths are not as large of a concern with f strings.  
* **Recommended Idioms**  
  * Always use new-style class declarations, i.e. always inherit from “object” if declaring a top-most class

```python
class Base(object):
    pass
```
Not
```python
class Base:
    pass
```

  * Prefer using super() over explicit base class names when invoking methods in base class. This will make your code more future-proof.
```python
class Base(object):
    def f(self):
        print('Base.f')

class Derived(Base):
    def f(self):
        super(Derived, self).f()  #<-- Do. Recommended
        Base.f(self)		  #<-- Don't. Discourage use.
        print('Drived.f')
```


  * Declare static and class methods using decorators, not old-style built-in functions
```python
class Test(object):
    @classmethod
    def f(class_type, value):
        pass

    @staticmethod
    def g(value):
        pass
```
Instead of:
```python
class Test(object):
    def f(class_type, value):
        pass
	
    f = classmethod(f)

    def g(value):
        pass

    g = classmethod(g)
```

* Don’t use sys.path.append or insert\!

# Unreal Engine

* Naming conventions   
  * Most studios and asset packs use similar or predictable naming conventions for UE  
  * Pascal casing  
  * Hungarian notation  
    * Used on the asset, and component level  
  * Notable exceptions are asset names that get directly presented to the user  
    * E.g. Editor Widgets  
  * Start broad, get narrow (T\_MyTexture\_BC\_01)  
* Macros only when absolutely necessary  
  * Strive to not use macros unless it has a direct benefit.  
* Graph readability  
  * Convenience over graph aesthetics  
    * Visual understanding more important than alignment  
    * Single responsibility per graph  
  * Return nodes, even if no return value to add high level graph clarity for the exit point of your functions.  
* Documentation  
  * Variables should have descriptions when necessary over comments  
    * Maps description (my key’s purpose : my value’s purpose)  
  * Comments are optional for describing a step or section of a graph but should prioritize describing why something exists rather than what it does  
  * Changelog  
    * Most assets/tools should have a changelog graph, or a manager or parent class with a changelog graph.
    Update descriptions should be logged in the changelist graph along with the corresponding version number.
