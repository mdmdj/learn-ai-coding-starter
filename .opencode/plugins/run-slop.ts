import { spawn } from "node:child_process";
import { Plugin } from "@opencode/plugin";

interface SlopResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

function runSloperator(cwd: string, file: string): Promise<SlopResult> {
  return new Promise((resolve) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", file], {
      cwd,
      shell: false,
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";
    let settled = false;

    const finish = (result: SlopResult) => {
      if (settled) return;
      settled = true;
      resolve(result);
    };

    child.stdout?.setEncoding("utf8");
    child.stderr?.setEncoding("utf8");
    child.stdout?.on("data", (chunk: string) => {
      stdout += chunk;
    });
    child.stderr?.on("data", (chunk: string) => {
      stderr += chunk;
    });

    child.on("error", (error) => {
      finish({ stdout, stderr: `${stderr}${error.message}`, exitCode: 1 });
    });

    child.on("close", (code, signal) => {
      finish({ stdout, stderr, exitCode: code ?? (signal ? 1 : 0) });
    });
  });
}

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a Sloperator (.slop) file and return its stdout, stderr, and exit code as JSON.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the .slop file, relative to the project root or absolute.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string };
          const result = await runSloperator(ctx.location.directory, path);
          return { content: JSON.stringify(result, null, 2) };
        },
      });
    });
  },
});
