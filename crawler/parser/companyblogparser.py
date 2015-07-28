# !/usr/bin/env python
# -*- coding: utf-8 -*-

from blogparser import BlogParser


class CompanyBlogParser(BlogParser):
    def __init__(self):
        BlogParser.__init__(self) ;

    def _parse_blog(self, blogsoup):
        # mid
        self.blog['mid'] = self._get_attr(blogsoup, 'mid')
        # mc
        msgsoup = blogsoup.find('div', attrs={'node-type': 'feed_list_content'})
        self.blog['mc'] = self._get_text(msgsoup)
        # rrc,rcc,rc,cc
        statsouplist = blogsoup.find_all('div', class_='WB_handle')
        if len(statsouplist) == 2:
            self.blog['rc'], self.blog['cc'] = self._parse_statistics(statsouplist[1])
            self.blog['rrc'], self.blog['rcc'] = self._parse_statistics(statsouplist[0])
        elif len(statsouplist) == 1:
            self.blog['rc'], self.blog['cc'] = self._parse_statistics(statsouplist[0])
        # run, ruid
        ruinfosoup = blogsoup.find(attrs={'node-type': 'feed_list_originNick'})
        if ruinfosoup:
            self.blog['run'] = self._get_attr(ruinfosoup, 'nick-name')
            self.blog['ruid'] = self._get_attr(ruinfosoup, 'usercard')
        # rmc
        rmcsoup = blogsoup.find(attrs={'node-type': 'feed_list_reason'})
        self.blog['rmc'] = self._get_text(rmcsoup)
        # rpt,rpage,page,pt,srn
        fromsouplist = blogsoup.find_all('div', class_='WB_from')
        if len(fromsouplist) == 2:
            page, pt, srn = self._parse_blog_from(fromsouplist[0])
            self.blog['rpage'] = page
            self.blog['rpt'] = pt
            self.blog['page'], self.blog['pt'], self.blog['srn'] = self._parse_blog_from(fromsouplist[1])
        elif len(fromsouplist) == 1:
            self.blog['page'], self.blog['pt'], self.blog['srn'] = self._parse_blog_from(fromsouplist[0])