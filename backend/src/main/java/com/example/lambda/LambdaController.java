package com.example.lambda;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.util.Map;

@RestController
@RequestMapping("/functions")
public class LambdaController {
    private final LambdaService lambdaService;

    @Autowired
    public LambdaController(LambdaService lambdaService) {
        this.lambdaService = lambdaService;
    }

    @PostMapping
    public ResponseEntity<?> deployFunction(
            @RequestParam("name") String name,
            @RequestParam("runtime") String runtime,
            @RequestParam("handler") String handler,
            @RequestParam("code") MultipartFile code,
            @RequestParam(value = "memory", defaultValue = "128") int memory,
            @RequestParam(value = "timeout", defaultValue = "30") int timeout) {
        lambdaService.deployFunction(name, runtime, handler, code, memory, timeout);
        return ResponseEntity.ok().build();
    }

    @GetMapping
    public ResponseEntity<Map<String, LambdaFunction>> listFunctions() {
        return ResponseEntity.ok(lambdaService.listFunctions());
    }

    @PostMapping("/{name}/invoke")
    public ResponseEntity<String> invokeFunction(@PathVariable String name) {
        String result = lambdaService.invokeFunction(name);
        return ResponseEntity.ok(result);
    }

    @DeleteMapping("/{name}")
    public ResponseEntity<?> deleteFunction(@PathVariable String name) {
        lambdaService.deleteFunction(name);
        return ResponseEntity.ok().build();
    }
} 