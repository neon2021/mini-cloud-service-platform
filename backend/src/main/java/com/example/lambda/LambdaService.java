package com.example.lambda;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Service
public class LambdaService {
    private final Map<String, LambdaFunction> functions = new ConcurrentHashMap<>();
    private final ExecutorService executorService = Executors.newCachedThreadPool();
    private final FunctionStorage storage;

    public LambdaService(FunctionStorage storage) {
        this.storage = storage;
    }

    public void deployFunction(String name, String runtime, String handler, 
                             MultipartFile code, int memory, int timeout) {
        LambdaFunction function = new LambdaFunction(name, runtime, handler, 
                                                   memory, timeout);
        storage.saveFunction(name, code);
        functions.put(name, function);
    }

    public String invokeFunction(String name) {
        LambdaFunction function = functions.get(name);
        if (function == null) {
            throw new RuntimeException("Function not found: " + name);
        }

        return executorService.submit(() -> {
            try {
                return function.execute(storage.getFunctionCode(name));
            } catch (Exception e) {
                throw new RuntimeException("Function execution failed", e);
            }
        }).get();
    }

    public void deleteFunction(String name) {
        functions.remove(name);
        storage.deleteFunction(name);
    }

    public Map<String, LambdaFunction> listFunctions() {
        return new ConcurrentHashMap<>(functions);
    }
} 