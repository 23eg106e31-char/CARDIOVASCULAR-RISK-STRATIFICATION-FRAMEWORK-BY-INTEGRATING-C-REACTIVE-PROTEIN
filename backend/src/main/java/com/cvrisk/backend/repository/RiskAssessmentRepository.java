package com.cvrisk.backend.repository;
import com.cvrisk.backend.entity.RiskAssessment; import org.springframework.data.jpa.repository.JpaRepository; import java.util.List;
public interface RiskAssessmentRepository extends JpaRepository<RiskAssessment,Long> { List<RiskAssessment> findTop50ByOrderByCreatedAtDesc(); }
