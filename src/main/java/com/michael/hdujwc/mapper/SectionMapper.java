package com.michael.hdujwc.mapper;

import com.michael.hdujwc.model.TTL;

import java.util.List;

public interface SectionMapper {
    List<TTL> getNews(String section);
}
