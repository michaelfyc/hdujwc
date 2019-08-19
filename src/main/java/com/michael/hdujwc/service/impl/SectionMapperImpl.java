package com.michael.hdujwc.service.impl;


import com.michael.hdujwc.mapper.SectionMapper;
import com.michael.hdujwc.model.TTL;
import com.michael.hdujwc.service.GetNews;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class SectionMapperImpl implements GetNews {
    @Resource
    SectionMapper sectionMapper;

    @Override
    public List<TTL> getNews(String section) {
        return sectionMapper.getNews(section);
    }
}
