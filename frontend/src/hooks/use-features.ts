/* eslint-disable @typescript-eslint/no-explicit-any */
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import type { FeatureResponse, FeatureCreate, Vote } from "@/lib/types";

export const useFeatures = () => {
  return useQuery<FeatureResponse[]>({
    queryKey: ["features"],
    queryFn: async () => {
      const { data } = await api.get("/features");
      return data;
    },
  });
};

export const useCreateFeature = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (feature: FeatureCreate) => {
      try {
        const { data } = await api.post("/features", feature);
        return data;
      } catch (error: any) {
        if (!error.response?.data?.error) {
          throw new Error(
            error.response?.data?.message ||
              error.message ||
              "Failed to create feature"
          );
        }
        throw error;
      }
    },
    onSuccess: () => {
      // Invalidate and refetch to ensure fresh data
      queryClient.invalidateQueries({ queryKey: ["features"] });
      queryClient.refetchQueries({ queryKey: ["features"] });
    },
  });
};

export const useVoteFeature = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ featureId }: { featureId: number }) => {
      try {
        const { data, status } = await api.post("/votes", {
          feature_id: featureId,
        });
        return { data, status };
      } catch (error: any) {
        console.error("Vote Error:", {
          status: error.response?.status,
          data: error.response?.data,
          error: error.message,
        });
        throw error;
      }
    },
    onSuccess: () => {
      // Properly invalidate queries to ensure data is refreshed
      queryClient.invalidateQueries({ queryKey: ["features"] });
      queryClient.invalidateQueries({ queryKey: ["votes"] });
      // Force a refetch to ensure we get fresh data
      queryClient.refetchQueries({ queryKey: ["features"] });
      queryClient.refetchQueries({ queryKey: ["votes"] });
    },
  });
};

export const useVotes = () => {
  return useQuery<Vote[]>({
    queryKey: ["votes"],
    queryFn: async () => {
      const { data } = await api.get("/votes");
      return data;
    },
  });
};
