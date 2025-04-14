import BasicFormRender from "@/components/Form/BasicFormRender";
import { ApiResponse, FormMetaType } from "@/types/general_types";
import { notify } from "@/utils/functions_utils";
import {
  DynamicRouter,
  deleteRequest,
  postRequest,
  putRequest,
} from "@/utils/request_utils";

import Loader from "@/components/components/general/Loader";
import { Button, FormInstance, Modal, Skeleton } from "antd";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import useSWR from "swr";

export default function WrapperCRUDForm({
  metadata,
  form,
  onFinish,
  buttonText,
  onCancel,
  mutationURL,
  onDeleteFinished,
}: {
  metadata: FormMetaType[];
  form?: FormInstance<any>;
  onFinish?: (values: any) => void;
  buttonText?: string;
  onCancel?: () => void;
  mutationURL: string;
  onDeleteFinished?: (response: any) => void;
}) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const params = useSearchParams();

  const record = {
    id: params.get("id") ?? undefined,
  };

  const isNewMode = params.get("new") === "True";
  const operation = isNewMode ? postRequest : putRequest;

  // Lookup URL'leri
  const rolesLookup = DynamicRouter("auth", "role");
  const organizationLookup = DynamicRouter("auth", "organization");
  const industryLookup = DynamicRouter("project", "industry");
  const serviceLookup = DynamicRouter("project", "service");
  const businessCycleLookup = DynamicRouter("project", "business-cycle");

  // Lookup verilerini al
  const { data: rolesData } = useSWR<ApiResponse<any>>(rolesLookup);
  const { data: organizationData } =
    useSWR<ApiResponse<any>>(organizationLookup);
  const { data: industryData } = useSWR<ApiResponse<any>>(industryLookup);
  const { data: serviceData } = useSWR<ApiResponse<any>>(serviceLookup);
  const { data: businessCycleData } =
    useSWR<ApiResponse<any>>(businessCycleLookup);

  // Düzenleme için veriyi al
  const { data: editData } = useSWR<ApiResponse<any>>(
    record.id ? `${mutationURL}${record.id}/` : null
  );

  // Lookup verilerini hazırla
  const lookup = {
    role:
      rolesData?.data?.map((role: any) => ({
        label: role.name,
        value: role.id,
      })) || [],
    organization:
      organizationData?.data?.map((org: any) => ({
        label: org.name,
        value: org.id,
      })) || [],
    industry: industryData?.data || [],
    service: serviceData?.data || [],
    business_cycle: businessCycleData?.data || [],
  };

  // Form verilerini doldur
  useEffect(() => {
    if (editData?.data?.[0] && form) {
      const formData = editData.data[0];

      // Form verilerini hazırla
      const formattedData = { ...formData };

      // Form alanlarını doldur
      form.resetFields(); // Önce formu temizle
      form.setFieldsValue(formattedData);
    }
  }, [editData, form]);

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      const submitUrl = record.id ? `${mutationURL}${record.id}/` : mutationURL;
      const response = await operation(submitUrl, { arg: values });
      if (onFinish) {
        onFinish(response);
      }
    } catch (error) {
      console.error("Form submission error:", error);
      notify("An error occurred while saving", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!record.id) return;
    try {
      setLoading(true);
      const deleteUrl = `${mutationURL}${record.id}/`;

      const response = await deleteRequest(deleteUrl);

      if (response.statusCode === 200) {
        if (onDeleteFinished) {
          onDeleteFinished(response);
        }
        setIsDeleteModalOpen(false);
        notify(response.message || "Record deleted successfully", "success");
      } else {
        notify(response.message || "Delete operation failed", "error");
        console.error("Delete failed:", response);
      }
    } catch (error) {
      // @ts-ignore
      notify(error?.message || "An error occurred while deleting", "error");
    } finally {
      setLoading(false);
    }
  };

  // Lookup verilerinin yüklenmesini bekle
  if (!lookup || Object.keys(lookup).length === 0) {
    return <Skeleton active />;
  }

  // Form verilerini hazırla
  const initialFormValues = editData?.data?.[0]
    ? { ...editData.data[0] }
    : undefined;
    
  if (record?.id && initialFormValues) {
    return (
      <Loader isLoading={loading}>
        <BasicFormRender
          metadata={metadata}
          form={form}
          onFinish={handleSubmit}
          onCancel={onCancel}
          buttonText={buttonText}
          initialValues={initialFormValues} 
          operation={operation}
          mutationURL={mutationURL}
          lookup={lookup}
        />
        {record.id && (
          <>
            <Button
              type="primary"
              danger
              block
              onClick={() => setIsDeleteModalOpen(true)}
              style={{ marginTop: 16 }}
            >
              Delete Record
            </Button>

            <Modal
              title="Delete Confirmation"
              open={isDeleteModalOpen}
              onOk={handleDelete}
              onCancel={() => setIsDeleteModalOpen(false)}
              okText="Delete"
              cancelText="Cancel"
              okButtonProps={{ danger: true }}
            >
              <p>Are you sure you want to delete this record?</p>
            </Modal>
          </>
        )}
      </Loader>
    );
  }
  return (
    <Loader isLoading={loading}>
      <BasicFormRender
        metadata={metadata}
        form={form}
        onFinish={handleSubmit}
        onCancel={onCancel}
        buttonText={buttonText}
        initialValues={initialFormValues} // Form başlangıç değerlerini ayarla
        operation={operation}
        mutationURL={mutationURL}
        lookup={lookup}
      />
      {record.id && (
        <>
          <Button
            type="primary"
            danger
            block
            onClick={() => setIsDeleteModalOpen(true)}
            style={{ marginTop: 16 }}
          >
            Delete Record
          </Button>

          <Modal
            title="Delete Confirmation"
            open={isDeleteModalOpen}
            onOk={handleDelete}
            onCancel={() => setIsDeleteModalOpen(false)}
            okText="Delete"
            cancelText="Cancel"
            okButtonProps={{ danger: true }}
          >
            <p>Are you sure you want to delete this record?</p>
          </Modal>
        </>
      )}
    </Loader>
  );
}
