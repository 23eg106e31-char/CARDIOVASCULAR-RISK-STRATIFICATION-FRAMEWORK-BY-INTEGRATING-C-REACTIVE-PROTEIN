package com.cvrisk.backend.exception;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import java.time.Instant;
import java.util.*;
@RestControllerAdvice
public class GlobalExceptionHandler {
 @ExceptionHandler(MethodArgumentNotValidException.class)
 public ResponseEntity<Map<String,Object>> handleValidation(MethodArgumentNotValidException ex) {
  Map<String,String> errors=new HashMap<>(); ex.getBindingResult().getFieldErrors().forEach(e->errors.put(e.getField(),e.getDefaultMessage()));
  Map<String,Object> body=new HashMap<>(); body.put("timestamp",Instant.now().toString()); body.put("status",400); body.put("error","Validation failed"); body.put("fieldErrors",errors); return ResponseEntity.badRequest().body(body);
 }
 @ExceptionHandler(MlServiceException.class)
 public ResponseEntity<Map<String,Object>> handleMl(MlServiceException ex) {
  Map<String,Object> body=new HashMap<>(); body.put("timestamp",Instant.now().toString()); body.put("status",502); body.put("error","ML service unavailable or errored"); body.put("message",ex.getMessage()); return ResponseEntity.status(HttpStatus.BAD_GATEWAY).body(body);
 }
 @ExceptionHandler(Exception.class)
 public ResponseEntity<Map<String,Object>> handleGeneric(Exception ex) {
  Map<String,Object> body=new HashMap<>(); body.put("timestamp",Instant.now().toString()); body.put("status",500); body.put("error","Internal server error"); body.put("message",ex.getMessage()); return ResponseEntity.internalServerError().body(body);
 }
}
