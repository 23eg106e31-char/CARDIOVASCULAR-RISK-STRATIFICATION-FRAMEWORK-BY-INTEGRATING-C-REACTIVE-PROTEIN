package com.cvrisk.backend.dto;
import lombok.Data; import java.util.List;
@Data public class RiskResponse { private Double predictedProbability; private String baseTier; private String crpCategory; private Boolean crpModifierApplied; private String finalTier; private List<TopFeature> topFeatures; }
