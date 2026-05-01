# Refactor Plan: tools/lib.rs → multi-module

## Target structure
```
tools/src/
├── lib.rs          # mod + re-exports only
├── registry.rs     # ToolRegistry, GlobalToolRegistry, ToolSpec, mvp_tool_specs(), deferred_tool_specs(), normalize helpers
├── dispatch.rs     # execute_tool(), run_* dispatchers, from_value, to_pretty_json, io_to_string
├── web.rs          # web_fetch + web_search: inputs, outputs, execution, helpers
├── todo.rs         # todo_write: inputs, outputs, execution
├── skill.rs        # skill: inputs, outputs, execution
├── agent.rs        # agent: inputs, outputs, execution
├── notebook.rs     # notebook_edit: inputs, outputs, execution
├── misc_tools.rs   # sleep, brief, config, structured_output, repl, powershell, tool_search
└── tests/          # or tests.rs at bottom of lib.rs
```

## Execution order
1. Create registry.rs (extract types + specs)
2. Create web.rs (extract web fetch/search)
3. Create todo.rs
4. Create skill.rs
5. Create agent.rs
6. Create notebook.rs
7. Create misc_tools.rs (sleep, brief, config, structured_output, repl, powershell, tool_search)
8. Create dispatch.rs (execute_tool + run_* wrappers)
9. Rewrite lib.rs (mod + re-exports)
10. cargo check → cargo test → fix issues

## Verification
- `cargo check --workspace` must pass
- `cargo test -p tools` must pass
- `cargo clippy -p tools` must not introduce new warnings
