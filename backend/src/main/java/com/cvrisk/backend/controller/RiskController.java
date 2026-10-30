package com.cvrisk.backend.controller;
import com.cvrisk.backend.dto.*; import com.cvrisk.backend.entity.RiskAssessment; import com.cvrisk.backend.repository.RiskAssessmentRepository; import com.cvrisk.backend.service.MlClientService; import jakarta.validation.Valid; import lombok.RequiredArgsConstructor; import org.springframework.web.bind.annotation.*; import java.util.*;
@RestController @RequestMapping("/api/risk") @RequiredArgsConstructor
public class RiskController {
 private final MlClientService mlClientService; private final RiskAssessmentRepository repository;
 @PostMapping("/assess") public RiskResponse assess(@Valid @RequestBody PatientRequest request){return mlClientService.scorePatient(request);}
 @GetMapping("/history") public List<RiskAssessment> history(){return repository.findTop50ByOrderByCreatedAtDesc();}
 @GetMapping("/health") public Map<String,String> health(){return Map.of("status","backend is up");}
}
