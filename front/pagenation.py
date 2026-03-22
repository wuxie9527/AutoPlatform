# coding=utf-8
"""
@Time : 2026/2/8 下午10:25
@Author : HeXW
"""
from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, currentPage='page', review_page=5):
        current_page = request.GET.get(currentPage, "1")
        if current_page.isdecimal():
                current_page = int(current_page)
        else:
                current_page = 1
        self.current_page = current_page
        self.page_size = page_size
        self.review_page = review_page

        self.start_indes = (current_page - 1) * page_size
        self.end_index = current_page * page_size
        print("="*30)
        print(self.start_indes,self.end_index)
        self.page_queryset = queryset[self.start_indes:self.end_index]
        total_page_num, div = divmod(queryset.count(), page_size)
        if div:
            total_page_num += 1
        self.total_page_num = total_page_num


    def html(self):
        if self.total_page_num <= 2 * self.review_page + 1:
            # 数据库数据比较少
            start_review_page = 1
            end_review_page = self.total_page_num
        else:
            # 处理小极值
            if self.current_page <= self.review_page:
                start_review_page = 1
                end_review_page = 2 * self.review_page

            else:
                # 当前页+review_page大于总页数
                if self.current_page + self.review_page > self.total_page_num:
                    end_review_page = self.total_page_num - 1
                    start_review_page = self.total_page_num - 2 * self.review_page
                else:
                    start_review_page = self.current_page - self.review_page
                    end_review_page = self.current_page + self.review_page - 1

        page_start_list = []
        # 首页
        first_page = f'<li><a href="?page={1}"> 首页 </a></li>'
        page_start_list.append(first_page)
        # 上一页
        if self.current_page > 1:
            prev = f'<li><a href="?page={self.current_page - 1}"> 上一页 </a></li>'
        else:
            prev = f'<li><a href="?page={1}">上一页</a></li>'
        page_start_list.append(prev)
        for i in range(start_review_page, end_review_page + 1):
            if i == self.current_page:
                el = f'<li class="active"><a href="?page={i}">{i}</a></li>'
            else:
                el = f'<li><a href="?page={i}">{i}</a></li>'
            page_start_list.append(el)
        # 下一页
        if self.current_page < self.total_page_num:
            next_page = f'<li><a href="?page={self.current_page + 1}">下一页</a></li>'
        else:
            next_page = f'<li><a href="?page={self.total_page_num}">下一页</a></li>'
        page_start_list.append(next_page)
        # 尾页
        last_page = f'<li><a href="?page={self.total_page_num}">尾页</a></li>'
        page_start_list.append(last_page)
        page_string = mark_safe(''.join(page_start_list))
        return page_string