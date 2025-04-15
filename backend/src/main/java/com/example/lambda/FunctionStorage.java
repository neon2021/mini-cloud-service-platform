package com.example.lambda;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@Service
public class FunctionStorage {
    private final Path storagePath;

    public FunctionStorage() {
        this.storagePath = Paths.get("lambda-functions");
        try {
            Files.createDirectories(storagePath);
        } catch (IOException e) {
            throw new RuntimeException("Failed to create storage directory", e);
        }
    }

    public void saveFunction(String name, MultipartFile code) {
        try {
            Path functionPath = storagePath.resolve(name);
            Files.createDirectories(functionPath);
            Path codePath = functionPath.resolve("function.zip");
            code.transferTo(codePath);
        } catch (IOException e) {
            throw new RuntimeException("Failed to save function code", e);
        }
    }

    public String getFunctionCode(String name) {
        try {
            Path codePath = storagePath.resolve(name).resolve("function.zip");
            return new String(Files.readAllBytes(codePath));
        } catch (IOException e) {
            throw new RuntimeException("Failed to read function code", e);
        }
    }

    public void deleteFunction(String name) {
        try {
            Path functionPath = storagePath.resolve(name);
            Files.walk(functionPath)
                 .sorted((a, b) -> -a.compareTo(b))
                 .forEach(path -> {
                     try {
                         Files.delete(path);
                     } catch (IOException e) {
                         throw new RuntimeException("Failed to delete function", e);
                     }
                 });
        } catch (IOException e) {
            throw new RuntimeException("Failed to delete function", e);
        }
    }
} 