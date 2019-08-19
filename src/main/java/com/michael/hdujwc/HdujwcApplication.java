package com.michael.hdujwc;


import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@MapperScan("com.michael.hdujwc.mapper")
@EnableScheduling
public class HdujwcApplication {

    public static void main(String[] args) {
        SpringApplication.run(HdujwcApplication.class, args);
    }

}
