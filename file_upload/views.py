import uuid
import os
from django.shortcuts import render, redirect
from django.http import Http404, FileResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, FormView, CreateView
from django.utils.http import urlquote
from .form import FileUploadForm, FileUploadModelForm
from .models import File


# 展示上传文件（通用视图）
class FileListView(ListView):
    model = File
    context_object_name = "files"
    template_name = "file_upload/file_list.html"


# 展示上传文件（方法）
'''
def file_list(request):
    files = File.objects.all()
    context = dict()
    context['files'] = files
    return render(request, "file_upload/file_list.html", context)
'''


# 上传文件处理方法
def handle_uploaded_file(file):
    file_type = file.name.split(".")[-1]
    file_name = "{}.{}".format(uuid.uuid4().hex[:10], file_type)
    file_path = os.path.join("files", file_type, file_name)
    absolute_file_path = os.path.join('media', 'files', file_type, file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, "wb+") as destination:
        for chunck in file.chunks():
            destination.write(chunck)
    return file_path


# 普通表单上传文件（通用视图）
class FileFormView(FormView):
    form_class = FileUploadForm
    success_url = reverse_lazy("file_upload:file_list")
    template_name = "file_upload/form_upload.html"

    def form_valid(self, form):
        file = File()
        file.title = form.cleaned_data['title']
        file_upload = form.cleaned_data['file']
        file.file = handle_uploaded_file(file_upload)
        file.save()
        return super().form_valid(form)


# 普通表单上传文件（方法）
'''
def form_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            file_upload = form.cleaned_data['file']
            file = File()
            file.file = handle_uploaded_file(file_upload)
            file.title = title
            file.save()
            return redirect("file_upload:file_list")
    else:
        form = FileUploadForm()
    context = dict()
    context['form'] = form
    context['title'] = "普通表单上传文件"
    return render(request, "file_upload/form_upload.html", context)
'''


# 使用ModelForm上传文件（通用视图）
class FileCreateView(CreateView):
    model = File
    fields = ['title', 'file']
    success_url = reverse_lazy("file_upload:file_list")
    template_name = "file_upload/form_upload.html"


# 使用ModelForm上传文件方法
'''
def form_upload_by_model_form(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("file_upload:file_list")
    else:
        form = FileUploadModelForm()
    context = dict()
    context['title'] = "普通表单上传文件"
    context['form'] = form
    return render(request, "file_upload/form_upload.html", context)
'''


# 文件删除（通用视图）
class FileDeleteView(DeleteView):
    model = File
    context_object_name = "file"
    success_url = reverse_lazy("file_upload:file_list")
    template_name = "file_upload/delete_file.html"

    def get_success_url(self):
        file = File.objects.get(pk=self.kwargs['pk'])
        file_dir = os.path.join("media", str(file.file))
        os.remove(file_dir)
        return super().get_success_url()


# 文件下载
def file_download(request, file_path):
    file = File.objects.get(file=file_path)
    file_path = os.path.join("media", file_path)
    file_type = file_path.split('.')[-1]
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = "attachment; filename={0}.{1}".format(urlquote(file.title), file_type)
        return response
    except Exception:
        raise Http404

