# Zoo Example
This is a simple software that lists animals in the zoo. 
As a developer, we try to put distinct modules into different sections.
In this way, we create layered architecture.

In the example, `bar/zoo.py` needs `foo/animals.py` to list animals in the zoo.
But, the reverse is not true. `foo` does not depend on `bar`. Depcheck library 
helps you to make sure that this dependency is hold. By defining rules like:
```yaml
layers:
  layer_1:
    - root.foo
  layer_2:
    - root.bar
whitelist:
  layer_1: ~
  layer_2:
    - layer_1
```
we can separate the application into distinct layers. In the `whitelist` section, we tell that: 
- Every packages added into `layer_1` should not depend on anything.
- The packages added into `layer_2` may depend on the packages inside `layer_1`.
