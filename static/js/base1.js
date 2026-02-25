$(document).ready(function() {
            // 导航菜单点击效果
            $('.sidebar .nav li').click(function() {
                $('.sidebar .nav li').removeClass('active');
                $(this).addClass('active');
            });




            $(document).ready(function() {
                // 全选/全不选功能
            $('#select-all').change(function() {
                var isChecked = $(this).prop('checked');
                $('.case-select').prop('checked', isChecked);
            });
                // 单个复选框变化时更新全选状态
            $('.case-select').change(function() {
                var total = $('.case-select').length;
                var checked = $('.case-select:checked').length;

                if (checked === total) {
                    $('#select-all').prop('checked', true);
                } else if (checked === 0) {
                    $('#select-all').prop('checked', false);
                } else {
                    $('#select-all').prop('indeterminate', true);
                }
            });

            });



            // 操作按钮事件
            // $('.action-item').click(function() {
            //     var actionText = $(this).find('.action-text').text();
            //     var caseId = $(this).closest('tr').find('.case-select').data('id');
            //
            //     if (actionText === '修改') {
            //         alert('修改用例 ' + caseId);
            //     } else if (actionText === '复制') {
            //         alert('复制用例 ' + caseId);
            //     } else if (actionText === '删除') {
            //         if (confirm('确定要删除用例 ' + caseId + ' 吗？')) {
            //             alert('删除成功');
            //             // 这里可以添加实际的删除逻辑
            //         }else {
            //              // 点击"取消"不执行任何操作
            //                 return;
            //     }
            // });

            // 测试按钮事件
            // $('.test-btn').click(function() {
            //     var caseId = $(this).closest('tr').find('.case-select').data('id');
            //     alert('测试用例 ' + caseId);
                // 这里可以添加实际的测试逻辑
            // });

            // 筛选表单提交
            // $('.filter-actions .btn-primary').click(function() {
            //     alert('执行查询操作');
                // 这里可以添加实际的AJAX查询逻辑
            // });

            // 重置按钮
            // $('.filter-actions .btn-default').click(function() {
            //     $('.filter-panel input').val('');
            //     $('.filter-panel select').val('');
            // });
        });