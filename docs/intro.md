# Contents
* [Introduction](#introduction)

# Introduction
This open-source project is about making a fully-fledged and modern IDE built on top of popular Vim editor. Already existing numerous features
found in Vim editor along with its powerful plugin engine will be used to carry out the features which can be found in more popular and
mainstream IDEs. In contrast, this IDE will additionally put focus on some specific requirements not being addressed by any other IDE.

## One to rule them all
Has it ever occurred to you to participate in a project(s) encompassing multiple platforms and/or technologies where each of them would impose a
requirement for specific development toolsets, such as different IDEs, toolchains, debuggers, build systems etc.? If it has, then you will
know how valuable would be to have a single and open-source product which could be utilized for whole such development. Why? There are numerous
reasons behind it but development targeting various platforms is usually done in very specialized, and very often commercial, IDEs which:
* mostly put focus on development for a particular platform
* do not support development for any other platform or provide a very limited support
* contain only a subset of features usually found in more advanced and mainstream IDEs
* are not easily extensible by the community
* are proprietary
* etc.

Having a standard and unified product would mitigate the aforementioned problems, but will also make you not to unnecessary waste your precious 
time by constantly re-learning the same tools. This is a pretty much common scenario if you are performing in dynamic work environment 
(i.e. short-term projects). So, one of the main goals of this project will be to build a single toolset which will provide an integrated 
environment to develop code no matter what platform is targeted for, such as:
* `bare-metal`,
* `RTOS`,
* `embedded-Linux`,
* `Android`,
* `desktop Linux, OS X, Windows, ...`

## Large-scale software
Moreover, there is yet to be seen an IDE which can cope with a code base as large and as complex as Android. This is what you definitely 
want to have if you do Android platform development. No IDE which has been set to that challenge was able to handle it. Be it Eclipse, 
Qt Creator or Codelite, each one of them would crash on a 64-bit Intel-i5 @2.5GHz machine with 12GB of RAM. Crash would always occur 
during the very basic operation: creating a new project and importing an existing Android source code. In either case, RAM would be 
eventually eaten up, probably by background source code indexing services, resulting in an application and/or system freeze.
This IDE will not get you into such problems.

## Mixed programming languages software
And what about projects such as Android containing source code written in multiple programming languages? IDEs present on the market, or
at least those that I am aware of, are usually able to handle single programming language per project. This in turn has a consequence of 
making the source code indexing service ignore all of the source code written in other programming languages and thus making impossible 
to utilize a whole lot of IDE features on such code (i.e. `find symbol references`, `go to definition`, `auto-complete` and alike).
To give you an example, one could easily imagine a project which features a middleware written in Java and all other platform-specific or 
performance-wise stuff written in some of the native programming languages such as C or C++. If one is employed in developing code for 
the whole stack, it would be very limiting to have IDE features working only for the subset of programming languages used in the project. 
This is a very important issue which has been genuinely addressed by this IDE.

## Good software design principles
Besides the aforementioned points, this IDE will also provide a complete development environment which will incorporate a programmers toolkit
which provides more seamless way to design better software. For example, it will integrate tools for:
* source code static analysis,
* unit-testing,
* source code management systems,
* docs generation

## Open-source at its finest
One may ask themselves is it really possible and realistic task to build a full-blown IDE in a reasonable time by a single developer? 
Thanks to the huge amount of open-source software which can be re-used and perfectly fitted into the IDE features, I think there is no 
space for doubt. Let me list just some of the open-source software this IDE relies on: `Vim`, `GNU GCC`, `Clang`, `GDB`, `LLDB`, 
`GNU Make`, `ctags`, `cscope`, `gtags`, `cppcheck`, `clang-analyzer`, `Git`, etc. Having in mind that open-source became a main driver
in nowadays technology advances, this list will only get bigger and better.

