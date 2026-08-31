"use client";

import { cn } from "@/lib/utils";
import { PIPELINE_STEPS } from "@/types/pipeline";
import type { PipelineJob } from "@/types/pipeline";

interface Props {
  steps: Record<string, PipelineJob | null>;
  activeStep: string;
  onStepClick: (step: string) => void;
}

function getStepStatus(job: PipelineJob | null | undefined): string {
  if (!job) return "pending";
  return job.status;
}

function StatusIcon({ status }: { status: string }) {
  if (status === "done") {
    return (
      <svg className="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
      </svg>
    );
  }
  if (status === "running") {
    return (
      <svg className="h-5 w-5 animate-spin text-blue-600" fill="none" viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
    );
  }
  if (status === "failed") {
    return (
      <svg className="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
      </svg>
    );
  }
  return (
    <div className="h-5 w-5 rounded-full border-2 border-gray-300" />
  );
}

export function PipelineSteps({ steps, activeStep, onStepClick }: Props) {
  return (
    <div className="flex items-center gap-0 rounded-lg border bg-white p-2">
      {PIPELINE_STEPS.map((step, index) => {
        const status = getStepStatus(steps[step.key]);
        const isActive = activeStep === step.key;

        return (
          <div key={step.key} className="flex items-center">
            <button
              onClick={() => onStepClick(step.key)}
              className={cn(
                "flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-gray-900 text-white"
                  : "text-gray-600 hover:bg-gray-100"
              )}
            >
              <StatusIcon status={status} />
              {step.label}
            </button>
            {index < PIPELINE_STEPS.length - 1 && (
              <svg className="mx-1 h-4 w-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            )}
          </div>
        );
      })}
    </div>
  );
}
