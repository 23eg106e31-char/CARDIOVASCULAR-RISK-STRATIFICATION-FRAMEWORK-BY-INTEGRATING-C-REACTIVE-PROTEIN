package com.cvrisk.backend.service;
import com.cvrisk.backend.dto.*; import com.cvrisk.backend.entity.RiskAssessment; import com.cvrisk.backend.exception.MlServiceException; import com.cvrisk.backend.repository.RiskAssessmentRepository; import lombok.RequiredArgsConstructor; import org.springframework.stereotype.Service; import org.springframework.web.reactive.function.client.WebClient; import org.springframework.web.reactive.function.client.WebClientResponseException;
@Service @RequiredArgsConstructor
public class MlClientService {
 private final WebClient mlServiceWebClient; private final RiskAssessmentRepository repository;
 public RiskResponse scorePatient(PatientRequest request){
  MlServiceResponse ml; try { ml=mlServiceWebClient.post().uri("/predict").bodyValue(MlServiceRequest.fromPatientRequest(request)).retrieve().bodyToMono(MlServiceResponse.class).block(); }
  catch(WebClientResponseException e){throw new MlServiceException("ML service returned an error ("+e.getStatusCode()+"): "+e.getResponseBodyAsString(),e);}
  catch(Exception e){throw new MlServiceException("Could not reach the ML service. Is it running on the configured ml.service.base-url?",e);}
  if(ml==null) throw new MlServiceException("ML service returned an empty response.");
  RiskResponse r=new RiskResponse(); r.setPredictedProbability(ml.getPredictedProbability());r.setBaseTier(ml.getBaseTier());r.setCrpCategory(ml.getCrpCategory());r.setCrpModifierApplied(ml.getCrpModifierApplied());r.setFinalTier(ml.getFinalTier());r.setTopFeatures(ml.getTopFeatures());
  RiskAssessment e=new RiskAssessment();e.setAge(request.getAge());e.setSex(request.getSex());e.setCrp(request.getCrp());e.setPredictedProbability(ml.getPredictedProbability());e.setBaseTier(ml.getBaseTier());e.setCrpCategory(ml.getCrpCategory());e.setCrpModifierApplied(ml.getCrpModifierApplied());e.setFinalTier(ml.getFinalTier());repository.save(e); return r;
 }
}
