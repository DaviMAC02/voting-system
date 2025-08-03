import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useCreateFeature } from "@/hooks/use-features";
import type { FeatureCreate, APIError } from "@/lib/types";

interface CreateFeatureFormProps {
  onSuccess?: () => void;
}

export function CreateFeatureForm({ onSuccess }: CreateFeatureFormProps) {
  const { mutate: createFeature, isPending } = useCreateFeature();
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);

    const form = e.currentTarget;
    const formData = new FormData(form);
    const feature: FeatureCreate = {
      title: formData.get("title") as string,
      description: formData.get("description") as string,
      category: formData.get("category") as "BUG" | "FEATURE" | "ENHANCEMENT",
    };

    createFeature(feature, {
      onSuccess: () => {
        form.reset();
        setError(null);
        onSuccess?.();
      },
      onError: (err: unknown) => {
        console.error("Form Error:", err);
        if (err instanceof Error) {
          setError(err.message);
        } else {
          const apiError = err as APIError;
          if (apiError.response?.data?.error) {
            setError(apiError.response.data.error);
          } else if (apiError.response?.data?.message) {
            setError(apiError.response.data.message);
          } else {
            setError("Failed to create feature");
          }
        }
      },
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium mb-1">
          Title
        </label>
        <input
          type="text"
          id="title"
          name="title"
          required
          className="w-full px-3 py-2 border rounded-md"
          placeholder="Enter feature title"
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium mb-1">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          required
          className="w-full px-3 py-2 border rounded-md"
          rows={3}
          placeholder="Describe the feature"
        />
      </div>

      <div>
        <label htmlFor="category" className="block text-sm font-medium mb-1">
          Category
        </label>
        <select
          id="category"
          name="category"
          required
          className="w-full px-3 py-2 border rounded-md"
        >
          <option value="BUG">Bug</option>
          <option value="FEATURE">Feature</option>
          <option value="ENHANCEMENT">Enhancement</option>
        </select>
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <Button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create Feature"}
      </Button>
    </form>
  );
}
