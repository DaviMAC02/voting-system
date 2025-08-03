import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/stores/auth";
import type { FeatureResponse, Vote } from "@/lib/types";
import { useVoteFeature, useVotes } from "@/hooks/use-features";
import { cn } from "@/lib/utils";
import { Heart } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface FeatureCardProps {
  feature: FeatureResponse;
}

export function FeatureCard({ feature }: FeatureCardProps) {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { mutate: vote, isPending: isVoting } = useVoteFeature();
  const { data: votes } = useVotes();
  const [optimisticVotes, setOptimisticVotes] = useState(feature.like_count);

  const userVote =
    user &&
    votes?.find(
      (v: Vote) => v.feature_id === feature.id && v.user_id === user.id
    );

  const handleLike = () => {
    if (!user) {
      navigate("/login");
      return;
    }

    const currentLikes = optimisticVotes;
    const likeChange = userVote ? -1 : 1;
    setOptimisticVotes(currentLikes + likeChange);

    vote(
      { featureId: feature.id },
      {
        onError: () => setOptimisticVotes(currentLikes),
      }
    );
  };

  return (
    <div className="rounded-lg border bg-card p-4 text-card-foreground shadow-sm">
      <div className="flex gap-4">
        <div className="flex flex-col items-center gap-2">
          <Button
            variant={userVote ? "default" : "outline"}
            size="icon"
            className="h-8 w-8"
            disabled={isVoting || !user}
            onClick={handleLike}
          >
            <Heart
              className={cn("h-4 w-4", {
                "text-primary-foreground fill-current": userVote,
              })}
            />
          </Button>
          <span className="text-sm font-medium">{optimisticVotes}</span>
        </div>

        <div className="flex-1">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="font-semibold">{feature.title}</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                {feature.description}
              </p>
            </div>
            <span
              className={cn(
                "rounded-full px-2 py-1 text-xs font-medium",
                feature.status === "Open"
                  ? "bg-green-100 text-green-700"
                  : "bg-red-100 text-red-700"
              )}
            >
              {feature.status}
            </span>
          </div>
          <div className="mt-2 text-xs text-muted-foreground">
            <span
              className={cn(
                "rounded-full px-2 py-1",
                feature.category === "BUG"
                  ? "bg-red-100 text-red-700"
                  : feature.category === "FEATURE"
                  ? "bg-blue-100 text-blue-700"
                  : "bg-purple-100 text-purple-700"
              )}
            >
              {feature.category}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
export default FeatureCard;
