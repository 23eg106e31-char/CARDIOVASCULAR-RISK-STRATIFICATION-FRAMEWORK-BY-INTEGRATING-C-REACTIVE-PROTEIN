package com.cvrisk.backend.dto;
import lombok.Data;
@Data public class MlServiceRequest {
 private Double age,bmi,systolicBp,diastolicBp,totalCholesterol,hdlCholesterol,ldlCholesterol,triglycerides,fastingGlucose,hba1c,crp;
 private Integer sex,smoker,diabetes,hypertensionTreated,familyHistoryCvd;
 private Double physicalActivityScore;
 public static MlServiceRequest fromPatientRequest(PatientRequest p){
  MlServiceRequest r=new MlServiceRequest(); r.age=p.getAge();r.sex=p.getSex();r.bmi=p.getBmi();r.systolicBp=p.getSystolicBp();r.diastolicBp=p.getDiastolicBp();r.totalCholesterol=p.getTotalCholesterol();r.hdlCholesterol=p.getHdlCholesterol();r.ldlCholesterol=p.getLdlCholesterol();r.triglycerides=p.getTriglycerides();r.fastingGlucose=p.getFastingGlucose();r.hba1c=p.getHba1c();r.crp=p.getCrp();r.smoker=p.getSmoker();r.diabetes=p.getDiabetes();r.hypertensionTreated=p.getHypertensionTreated();r.familyHistoryCvd=p.getFamilyHistoryCvd();r.physicalActivityScore=p.getPhysicalActivityScore(); return r;
 }
}
