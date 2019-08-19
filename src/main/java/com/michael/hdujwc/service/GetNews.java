package com.michael.hdujwc.service;

import com.michael.hdujwc.model.TTL;

import java.util.List;

public interface GetNews {
    List<TTL> getNews(String section);
}
