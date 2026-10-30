package com.cvrisk.backend.config;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;
import java.time.Duration;
@Configuration
public class WebClientConfig {
  @Value("${ml.service.base-url}") private String mlServiceBaseUrl;
  @Bean public WebClient mlServiceWebClient() {
    HttpClient httpClient = HttpClient.create().responseTimeout(Duration.ofSeconds(30));
    return WebClient.builder().baseUrl(mlServiceBaseUrl).clientConnector(new ReactorClientHttpConnector(httpClient)).build();
  }
}
