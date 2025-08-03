import { useState } from "react";
import { useFeatures } from "@/hooks/use-features";
import { FeatureCard } from "./feature-card";
import { CreateFeatureForm } from "./create-feature-form";
import { Button } from "./ui/button";
import { useAuth } from "@/stores/auth";
import type { FeatureResponse } from "@/lib/types";

export function FeatureList() {
  const { data: features, isLoading, error } = useFeatures();
  const { user } = useAuth();
  const [showForm, setShowForm] = useState(false);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-r-transparent" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center p-8 text-destructive">
        Failed to load features
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {user && (
        <div>
          {!showForm ? (
            <div className="flex justify-end mb-6">
              <Button onClick={() => setShowForm(true)}>+ New Feature</Button>
            </div>
          ) : (
            <div className="rounded-lg border p-4 mb-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Create New Feature</h2>
                <Button variant="outline" onClick={() => setShowForm(false)}>
                  Cancel
                </Button>
              </div>
              <CreateFeatureForm onSuccess={() => setShowForm(false)} />
            </div>
          )}
        </div>
      )}

      {!features?.length ? (
        <div className="flex items-center justify-center p-8 text-muted-foreground">
          {user
            ? "No features yet. Create the first one!"
            : "No features found"}
        </div>
      ) : (
        <div className="grid gap-4">
          {features.map((feature: FeatureResponse) => (
            <FeatureCard key={feature.id} feature={feature} />
          ))}
        </div>
      )}
    </div>
  );
}
