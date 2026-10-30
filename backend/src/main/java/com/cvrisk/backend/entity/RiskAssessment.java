package com.cvrisk.backend.entity;
import jakarta.persistence.*; import lombok.Data; import lombok.NoArgsConstructor; import java.time.Instant;
@Entity @Table(name="risk_assessments") @Data @NoArgsConstructor
public class RiskAssessment {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
 private Double age; private Integer sex; private Double crp; private Double predictedProbability; private String baseTier; private String crpCategory; private Boolean crpModifierApplied; private String finalTier; private Instant createdAt=Instant.now();
}
