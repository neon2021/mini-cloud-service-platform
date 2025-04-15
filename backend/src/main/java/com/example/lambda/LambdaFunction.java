package com.example.lambda;

public class LambdaFunction {
    private final String name;
    private final String runtime;
    private final String handler;
    private final int memory;
    private final int timeout;

    public LambdaFunction(String name, String runtime, String handler, 
                         int memory, int timeout) {
        this.name = name;
        this.runtime = runtime;
        this.handler = handler;
        this.memory = memory;
        this.timeout = timeout;
    }

    public String execute(String code) {
        // TODO: Implement function execution based on runtime
        // This is a placeholder implementation
        return "Function " + name + " executed successfully";
    }

    public String getName() {
        return name;
    }

    public String getRuntime() {
        return runtime;
    }

    public String getHandler() {
        return handler;
    }

    public int getMemory() {
        return memory;
    }

    public int getTimeout() {
        return timeout;
    }
} 