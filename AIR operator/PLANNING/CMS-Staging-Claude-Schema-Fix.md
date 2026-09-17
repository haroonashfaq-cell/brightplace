# CMS staging: Claude Code tool-schema rejection

Date: 16 September 2026
Status: diagnosed from local logs; server schema fix not yet implemented

## Confirmed

Claude Code successfully connected to `claude.ai brightplace CMS - Staging`, identifying the server as Operator Hub 1.0.0. After tool search loaded CMS definitions, Anthropic rejected the model request:

```text
tools.25.custom.input_schema: input_schema does not support oneOf, allOf, or anyOf at the top level
request_id: req_011Cf7qUiwNN7rQYon4W8zzo
```

The matching log records tool search at 21:34:36 UTC followed by the rejection at 21:34:37 UTC. This is a schema compatibility failure after connection, not an authentication failure. Repeated prompts fail because the incompatible tool definition is still included.

The session contains these CMS tool references: `blog_validate_post`, `brief_get`, `brief_list`, `brief_save`, `operator_context_get`. These are candidates to inspect, not confirmed offenders. No raw server schemas were available in this inspection. `tools.25` identifies a position in that request's combined tool list, not a stable CMS tool name; earlier failures used position 39.

## Immediate recovery

In Claude Code, open `/mcp`, select the display name `claude.ai brightplace CMS - Staging` and disable that connector for the project. Start a fresh session if the current conversation still includes the rejected definition. Keep its saved connection configuration so it can be re-enabled after the fix.

The connector is delivered through Claude.ai, rather than listed as a local CMS entry in the project's MCP configuration. Prefer the `/mcp` toggle over assuming `claude mcp remove` will remove this connector.

Source: [Claude Code MCP controls](https://code.claude.com/docs/en/mcp#disable-a-server-without-removing-it).

## Developer action

1. Retrieve all pages of staging `tools/list` using the affected identity.
2. Inspect each tool's emitted `inputSchema`, specifically root-level `oneOf`, `anyOf` and `allOf`. Check the serialized output, not only source Zod/TypeScript definitions.
3. Export a root object schema compatible with Claude. For operation variants, prefer separate tools, or explicit object fields and a discriminator with operation-specific server validation. Nested composition may be an option only after verifying the target client's supported subset.
4. Do not simply delete composition keywords: doing so can discard required fields and validation. Preserve mutually exclusive/operation-specific constraints in the handler or revised schema.
5. Add a contract regression check over all exported tool schemas. Reject incompatible root composition and verify object roots as part of the supported Claude contract.
6. Redeploy staging and refresh/reconnect the connector in a fresh Claude Code session.

Source: [Anthropic tool definitions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools). The exact top-level rejection above is confirmed by the API response, not inferred from general JSON Schema validity.

## Acceptance criteria

- Tools can be loaded through search in Claude Code without HTTP 400.
- A read-only `operator_context_get` call succeeds with the staging identity.
- Each revised tool still rejects invalid operation-specific payloads with an actionable error.
- Create/update variants retain their previous authorization, idempotency and concurrency checks.
- CMS functionality and validation are preserved; compatibility is not achieved by making inputs unrestricted.

## Message for the developer

> CMS staging connects in Claude Code, but Anthropic rejects a loaded tool schema with `tools.25.custom.input_schema: input_schema does not support oneOf, allOf, or anyOf at the top level`. Please inspect the emitted tools/list schemas, replace root composition with a Claude-compatible object contract while preserving operation validation, and add a regression check across all tools. The failing session loaded blog_validate_post, brief_get, brief_list, brief_save and operator_context_get, but the exact offending tool is not yet identified. Request ID: req_011Cf7qUiwNN7rQYon4W8zzo.
