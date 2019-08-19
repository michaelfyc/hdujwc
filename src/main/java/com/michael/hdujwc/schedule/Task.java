package com.michael.hdujwc.schedule;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class Task {
    private Logger logger = LoggerFactory.getLogger(Task.class);

    //每天8点执行
    @Scheduled(cron = "0 0 8 * * ?")
    public void crawlHDU() {
        try {
            logger.info("正在爬杭电教务处...");

            Runtime.getRuntime().exec("python -W ignore crawler.py");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
