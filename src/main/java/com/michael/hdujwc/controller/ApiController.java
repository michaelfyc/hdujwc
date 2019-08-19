package com.michael.hdujwc.controller;


import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.michael.hdujwc.model.TTL;
import com.michael.hdujwc.service.impl.SectionMapperImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class ApiController {
    private Logger logger = LoggerFactory.getLogger(ApiController.class);
    private static int LIMIT = 15;
    private static String SECTION = "together";
    private Map jsonMap = new HashMap(1);

    @Autowired
    SectionMapperImpl mapper;

    @GetMapping("/section")
    public Map section(String section, int page) {
        List<TTL> news = null;
        PageHelper.startPage(page, LIMIT);
        if (section == null) {
            news = mapper.getNews(SECTION);
        } else {
            news = mapper.getNews(section);
        }

        PageInfo<TTL> p = new PageInfo<>(news);
        jsonMap.put("data", news);
        jsonMap.put("count", p.getTotal());
        jsonMap.put("totalPage", p.getPages());
        jsonMap.put("isFirstPage", p.isIsFirstPage());
        jsonMap.put("isLastPage", p.isIsLastPage());
        jsonMap.put("pageNum", p.getPageNum());
        logger.info("对接口发起了请求...");
        return jsonMap;

    }


}
