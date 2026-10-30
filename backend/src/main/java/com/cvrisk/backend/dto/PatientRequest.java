package com.cvrisk.backend.dto;
import jakarta.validation.constraints.*; import lombok.Data;
@Data public class PatientRequest {
 @NotNull @Min(18) @Max(120) private Double age;
 @NotNull @Min(0) @Max(1) private Integer sex;
 @NotNull @DecimalMin("10") @DecimalMax("80") private Double bmi;
 @NotNull @DecimalMin("70") @DecimalMax("260") private Double systolicBp;
 @NotNull @DecimalMin("40") @DecimalMax("160") private Double diastolicBp;
 @NotNull @DecimalMin("50") @DecimalMax("500") private Double totalCholesterol;
 @NotNull @DecimalMin("10") @DecimalMax("150") private Double hdlCholesterol;
 @NotNull @DecimalMin("10") @DecimalMax("400") private Double ldlCholesterol;
 @NotNull @DecimalMin("20") @DecimalMax("1000") private Double triglycerides;
 @NotNull @DecimalMin("40") @DecimalMax("500") private Double fastingGlucose;
 @NotNull @DecimalMin("2") @DecimalMax("20") private Double hba1c;
 @NotNull @DecimalMin("0") @DecimalMax("100") private Double crp;
 @NotNull @Min(0) @Max(1) private Integer smoker;
 @NotNull @Min(0) @Max(1) private Integer diabetes;
 private Integer hypertensionTreated = 0;
 private Integer familyHistoryCvd = 0;
 private Double physicalActivityScore = 0.0;
}
