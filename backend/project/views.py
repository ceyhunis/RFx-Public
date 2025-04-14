from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from requestforproposalbackend.services.open_ai import ChatService
from requestforproposalbackend.services.email_js import EmailJSService
from authentication.models import Role, User, Organization
from project.models import *
from requestforproposalbackend.services.outseta import OutsetaService
from django.db.models import Q


from project.serializers import *
from requestforproposalbackend.api_response import api_response


class IndustryListCreateAPIView(ListCreateAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

    def get(self, request, *args, **kwargs):
        try:
            industries = Industry.objects.all()
            serializer = IndustrySerializer(industries, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Industries retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = IndustrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Industry created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class IndustryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

    def get(self, request, *args, **kwargs):
        try:
            industry = Industry.objects.get(pk=kwargs["pk"])
            serializer = IndustrySerializer(industry)
            response = api_response(
                [serializer.data],
                "success",
                message="Industry retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            industry = Industry.objects.get(pk=kwargs["pk"])
            serializer = IndustrySerializer(industry, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    [serializer.data],
                    "success",
                    message="Industry updated successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            industry = Industry.objects.get(pk=kwargs["pk"])
            industry.delete()
            response = api_response(
                None,
                "success",
                message="Industry deleted successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class ServiceListCreateAPIView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request, *args, **kwargs):
        try:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Services retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = ServiceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Service created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class ServiceDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request, *args, **kwargs):
        try:
            service = Service.objects.get(pk=kwargs["pk"])
            serializer = ServiceSerializer(service)
            response = api_response(
                [serializer.data],
                "success",
                message="Service retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            service = Service.objects.get(pk=kwargs["pk"])
            serializer = ServiceSerializer(service, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    [serializer.data],
                    "success",
                    message="Service updated successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            service = Service.objects.get(pk=kwargs["pk"])
            service.delete()
            response = api_response(
                None, "success", message="Service deleted successfully", status_code=200
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class CustomServiceListCreateAPIView(ListCreateAPIView):
    serializer_class = CustomServiceSerializer
    queryset = CustomService.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            services = CustomService.objects.filter(user_id=request.user.id)
            serializer = self.serializer_class(services, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Custom services retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data["user"] = request.user.id

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Custom service created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)

        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class CombinedServiceListCreateAPIView(APIView):

    def get(self, request, *args, **kwargs):
        organization_id = self.kwargs.get("id")

        services = Service.objects.all()
        custom_services = CustomService.objects.filter(organization_id=organization_id)

        if not organization_id:
            return Response(
                {"error": "Organization ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        services_serializer = ServiceSerializer(services, many=True)
        custom_services_serializer = CustomServiceSerializer(custom_services, many=True)

        return Response(
            {
                "services": services_serializer.data,
                "custom_services": custom_services_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CustomServiceDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            # Genel servisleri al
            services = Service.objects.all()
            services_serializer = ServiceSerializer(services, many=True)

            # Kullanıcının custom servislerini al
            custom_services = CustomService.objects.filter(user_id=pk)
            custom_services_serializer = CustomServiceSerializer(
                custom_services, many=True
            )

            # Her iki listeyi birleştir
            combined_data = services_serializer.data + custom_services_serializer.data

            response = api_response(
                combined_data,
                "success",
                message="Services retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)

        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, pk, *args, **kwargs):
        try:
            data = request.data.copy()
            data["user_id"] = pk  # Kullanıcı ID'sini ekle

            serializer = CustomServiceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Custom service created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)

        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class BusinessCycleListCreateAPIView(ListCreateAPIView):
    queryset = BusinessCycle.objects.all()
    serializer_class = BusinessCycleSerializer

    def get(self, request, *args, **kwargs):
        try:
            business_cycles = BusinessCycle.objects.all().order_by("order")
            serializer = BusinessCycleSerializer(business_cycles, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Business cycles retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = BusinessCycleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Business cycle created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class CustomBusinessCycleListCreateAPIView(ListCreateAPIView):
    serializer_class = CustomBusinessCycleSerializer
    queryset = CustomBusinessCycle.objects.all()

    def get(self):
        return queryset.objects.filter(user=self.request.user)

    def post(self, serializer):
        serializer.save(user=self.request.user)


class CombinedBusinessCycleListCreateAPIView(APIView):

    def get(self, request, *args, **kwargs):
        organization_id = self.kwargs.get("id")

        businessCycles = BusinessCycle.objects.all()
        custom_businessCycles = CustomBusinessCycle.objects.filter(
            organization_id=organization_id
        )

        if not organization_id:
            return Response(
                {"error": "Organization ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        businessCycles_serializer = BusinessCycleSerializer(businessCycles, many=True)
        custom_services_serializer = CustomBusinessCycleSerializer(
            custom_businessCycles, many=True
        )

        return Response(
            {
                "businessCycles": businessCycles_serializer.data,
                "custom_services": custom_services_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class BusinessCycleDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = BusinessCycle.objects.all()
    serializer_class = BusinessCycleSerializer

    def get(self, request, *args, **kwargs):
        try:
            business_cycle = BusinessCycle.objects.get(pk=kwargs["pk"])
            serializer = BusinessCycleSerializer(business_cycle)
            response = api_response(
                [serializer.data],
                "success",
                message="Business cycle retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            business_cycle = BusinessCycle.objects.get(pk=kwargs["pk"])
            serializer = BusinessCycleSerializer(business_cycle, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    [serializer.data],
                    "success",
                    message="Business cycle updated successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            business_cycle = BusinessCycle.objects.get(pk=kwargs["pk"])
            business_cycle.delete()
            response = api_response(
                None,
                "success",
                message="Business cycle deleted successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class CustomBusinessCycleDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            # Genel business cycle'ları al
            business_cycles = BusinessCycle.objects.all()
            business_cycles_serializer = BusinessCycleSerializer(
                business_cycles, many=True
            )

            # Kullanıcının custom business cycle'larını al
            custom_business_cycles = CustomBusinessCycle.objects.filter(user_id=pk)
            custom_business_cycles_serializer = CustomBusinessCycleSerializer(
                custom_business_cycles, many=True
            )

            # Her iki listeyi birleştir
            combined_data = (
                business_cycles_serializer.data + custom_business_cycles_serializer.data
            )

            response = api_response(
                combined_data,
                "success",
                message="Business cycles retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)

        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, pk, *args, **kwargs):
        try:
            data = request.data.copy()
            data["user_id"] = pk  # Kullanıcı ID'sini ekle

            serializer = CustomBusinessCycleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Custom business cycle created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)

        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class FunctionalAreaListCreateAPIView(ListCreateAPIView):
    queryset = FunctionalArea.objects.all().order_by("order")
    serializer_class = FunctionalAreaSerializer

    def get(self, request, *args, **kwargs):
        try:
            business_cycle_id = request.query_params.get("business_cycle_id")
            functional_areas = (
                FunctionalArea.objects.filter(
                    business_cycle_id=business_cycle_id
                ).order_by("order")
                if business_cycle_id
                else FunctionalArea.objects.all().order_by("order")
            )
            serializer = FunctionalAreaSerializer(functional_areas, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Functional areas retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = FunctionalAreaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Functional area created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                return Response(
                    api_response(None, "error", serializer.errors, 400),
                    status=400,
                )
        except Exception as e:
            return Response(
                api_response(None, "error", f"An error occurred: {str(e)}", 500),
                status=500,
            )


class FunctionalAreaDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = FunctionalArea.objects.all()
    serializer_class = FunctionalAreaSerializer

    def get(self, request, *args, **kwargs):
        try:
            functional_area = FunctionalArea.objects.get(pk=kwargs["pk"])
            serializer = FunctionalAreaSerializer(functional_area)
            response = api_response(
                [serializer.data],
                "success",
                message="Functional area retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            # Check if the record exists in CustomFunctionalArea
            try:
                custom_functional_area = CustomFunctionalArea.objects.get(
                    pk=kwargs["pk"]
                )
                serializer = CustomFunctionalAreaSerializer(
                    custom_functional_area, data=request.data
                )
            except CustomFunctionalArea.DoesNotExist:
                # If not found in CustomFunctionalArea, proceed with FunctionalArea
                functional_area = FunctionalArea.objects.get(pk=kwargs["pk"])
                serializer = FunctionalAreaSerializer(
                    functional_area, data=request.data
                )

            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    "Functional area updated successfully",
                    200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 400)
                return Response(response, status=400)
        except FunctionalArea.DoesNotExist:
            response = api_response(None, "error", "Functional area not found", 404)
            return Response(response, status=404)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            # Check if the record exists in CustomFunctionalArea
            try:
                custom_functional_area = CustomFunctionalArea.objects.get(
                    pk=kwargs["pk"]
                )
                custom_functional_area.delete()
            except CustomFunctionalArea.DoesNotExist:
                # If not found in CustomFunctionalArea, proceed with FunctionalArea
                functional_area = FunctionalArea.objects.get(pk=kwargs["pk"])
                functional_area.delete()

            response = api_response(
                None,
                "success",
                "Functional area deleted successfully",
                200,
            )
            return Response(response, status=200)
        except FunctionalArea.DoesNotExist:
            response = api_response(None, "error", "Functional area not found", 404)
            return Response(response, status=404)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class CustomFunctionalAreaListCreateAPIView(ListCreateAPIView):
    queryset = CustomFunctionalArea.objects.all()
    serializer_class = CustomFunctionalAreaSerializer

    def get(self, request, *args, **kwargs):
        try:
            organization_id = request.query_params.get("organization_id")

            # Base query to get null (general) records
            base_query = Q(organization__isnull=True)

            # If organization_id is provided, include records for that organization
            if organization_id:
                base_query |= Q(organization_id=organization_id)

            custom_functional_areas = CustomFunctionalArea.objects.filter(
                base_query
            ).order_by("order")

            serializer = CustomFunctionalAreaSerializer(
                custom_functional_areas, many=True
            )
            response = api_response(
                serializer.data,
                "success",
                message="Custom functional areas retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            # Log the incoming request data for debugging
            print("POST /custom-functional-area/ - Request data:", request.data)

            # Check if the request is from the admin panel with `new=True`
            if request.query_params.get("new") == "True":
                request.data["organization"] = None  # Set organization to null
            else:
                # Ensure organization_id is provided and valid for non-admin requests
                if (
                    "organization_id" in request.data
                    and request.data["organization_id"]
                ):
                    organization_id = request.data["organization_id"]
                    if not Organization.objects.filter(id=organization_id).exists():
                        print(
                            f"POST /custom-functional-area/ - Invalid organization_id: {organization_id}"
                        )
                        return Response(
                            api_response(None, "error", "Invalid organization ID", 400),
                            status=400,
                        )
                    request.data["organization"] = organization_id
                else:
                    request.data["organization"] = None  # Allow null organization

            # Log before serializer validation
            print(
                "POST /custom-functional-area/ - Validating serializer with data:",
                request.data,
            )
            serializer = CustomFunctionalAreaSerializer(data=request.data)
            if serializer.is_valid():
                # Log before saving the serializer
                print(
                    "POST /custom-functional-area/ - Serializer is valid. Saving data..."
                )
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Custom functional area created successfully",
                    status_code=200,
                )
                print(
                    "POST /custom-functional-area/ - Custom functional area created successfully:",
                    serializer.data,
                )
                return Response(response, status=200)
            else:
                # Log serializer errors for debugging
                print(
                    "POST /custom-functional-area/ - Serializer errors:",
                    serializer.errors,
                )
                response = api_response(None, "error", serializer.errors, 400)
                return Response(response, status=400)
        except Exception as e:
            # Log the exception for debugging
            print(f"POST /custom-functional-area/ - An error occurred: {str(e)}")
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def get_queryset(self):
        organization_id = self.request.user.organization_id
        if organization_id is None:
            # If the user has no organization_id, return only general custom functional areas
            return CustomFunctionalArea.objects.filter(
                organization_id__isnull=True
            ).order_by("order")
        # Return records for the user's organization_id and general records
        return CustomFunctionalArea.objects.filter(
            Q(organization_id=organization_id) | Q(organization_id__isnull=True)
        ).order_by("order")

    def perform_create(self, serializer):
        serializer.save(organization_id=self.request.user.organization_id)


class CustomFunctionalAreaDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CustomFunctionalArea.objects.all()
    serializer_class = CustomFunctionalAreaSerializer

    def get(self, request, *args, **kwargs):
        try:
            custom_functional_area = CustomFunctionalArea.objects.get(pk=kwargs["pk"])
            serializer = CustomFunctionalAreaSerializer(custom_functional_area)
            response = api_response(
                [serializer.data],
                "success",
                message="Custom functional area retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            custom_functional_area = CustomFunctionalArea.objects.get(pk=kwargs["pk"])
            serializer = CustomFunctionalAreaSerializer(
                custom_functional_area, data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    "Custom functional area updated successfully",
                    200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 400)
                return Response(response, status=400)
        except CustomFunctionalArea.DoesNotExist:
            response = api_response(
                None, "error", "Custom functional area not found", 404
            )
            return Response(response, status=404)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            custom_functional_area = CustomFunctionalArea.objects.get(pk=kwargs["pk"])
            custom_functional_area.delete()
            response = api_response(
                None,
                "success",
                "Custom functional area deleted successfully",
                200,
            )
            return Response(response, status=200)
        except CustomFunctionalArea.DoesNotExist:
            response = api_response(
                None, "error", "Custom functional area not found", 404
            )
            return Response(response, status=404)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class BulkActionsAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            table = request.data["table"]
            action = request.data["action"]
            ids = request.data["ids"]

            if action == "delete":
                if table == "business_cycle":
                    BusinessCycle.objects.filter(id__in=ids).delete()
                elif table == "industry":
                    Industry.objects.filter(id__in=ids).delete()
                elif table == "functional_area":
                    FunctionalArea.objects.filter(id__in=ids).delete()
                elif table == "role":
                    Role.objects.filter(id__in=ids).delete()
                elif table == "user":
                    User.objects.filter(id__in=ids).delete()
                elif table == "service":
                    Service.objects.filter(id__in=ids).delete()
                elif table == "organization":
                    Organization.objects.filter(id__in=ids).delete()
                elif table == "provider":
                    Provider.objects.filter(id__in=ids).delete()
                else:
                    raise Exception(f"Invalid table: {table}")

            response = api_response(
                None,
                "success",
                message=f"{str(action).upper()} action completed successfully",
                status_code=200,
            )
            return Response(response, status=200)

        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class SaveWithMultiDataAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data_list = request.data["data"]
            table = request.data["table"]
            if not isinstance(data_list, list):
                raise Exception("Data must be a list of items.")

            with transaction.atomic():
                for data in data_list[1:]:  # Ignore the first row
                    if table == "business_cycle":
                        if not BusinessCycle.objects.filter(name=data[1]).exists():
                            model_instance = BusinessCycle(
                                name=data[1], description=data[2], order=data[0]
                            )
                    elif table == "industry":
                        if not Industry.objects.filter(name=data[0]).exists():
                            model_instance = Industry(name=data[0], description=data[1])
                    elif table == "functional_area":
                        if not FunctionalArea.objects.filter(
                            name=data[0],
                            business_cycle_id=request.data["business_cycle_id"],
                        ).exists():
                            data_dict = {
                                "name": data[0],
                                "description": data[1],
                                "business_cycle_id": request.data["business_cycle_id"],
                            }
                            model_instance = FunctionalArea(**data_dict)
                    elif table == "service":
                        if not Service.objects.filter(name=data[0]).exists():
                            model_instance = Service(name=data[0], description=data[1])
                    else:
                        raise Exception("Invalid table")

                    if "model_instance" in locals():
                        model_instance.full_clean()
                        model_instance.save()
                        del model_instance  # Remove the instance to avoid reuse in the next iteration

            response = api_response(
                None,
                "success",
                message=f"{str(table).upper()} saved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class GeneratedRFPCreateView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            if request.query_params:
                params = {
                    key: value
                    for key, value in request.query_params.items()
                    if value is not None
                }
                generated_rfps = GeneratedRFP.objects.filter(**params)
                serializer = GeneratedRFPSerializer(generated_rfps, many=True)
                response = api_response(
                    serializer.data,
                    "success",
                    message="Generated RFP retrieved successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            generated_rfps = GeneratedRFP.objects.all()
            serializer = GeneratedRFPSerializer(generated_rfps, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Generated RFP retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = GeneratedRFPSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Generated RFP created successfully",
                    status_code=200,
                )
                return Response(response, status=200)

            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)

        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class GeneratedRFPDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = GeneratedRFP.objects.all()
    serializer_class = GeneratedRFPSerializer

    def get(self, request, *args, **kwargs):
        try:
            generated_rfp = GeneratedRFP.objects.get(pk=kwargs["pk"])
            serializer = self.get_serializer(generated_rfp)
            response = api_response(
                serializer.data,
                "success",
                "Generated RFP retrieved successfully",
                200,
            )
            return Response(response, status=200)
        except GeneratedRFP.DoesNotExist:
            response = api_response(None, "error", "Generated RFP not found", 404)
            return Response(response, status=404)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            generated_rfp = GeneratedRFP.objects.get(pk=kwargs["pk"])
            serializer = self.get_serializer(generated_rfp, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    "Generated RFP updated successfully",
                    200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 400)
                return Response(response, status=400)
        except GeneratedRFP.DoesNotExist:
            response = api_response(None, "error", "Generated RFP not found", 404)
            return Response(response, status=404)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            generated_rfp = GeneratedRFP.objects.get(pk=kwargs["pk"])
            generated_rfp.delete()
            response = api_response(
                None, "success", "Generated RFP deleted successfully", 200
            )
            return Response(response, status=200)
        except GeneratedRFP.DoesNotExist:
            response = api_response(None, "error", "Generated RFP not found", 404)
            return Response(response, status=404)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class SubmittedRFPCreateView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            if request.query_params:
                params = {
                    key: value
                    for key, value in request.query_params.items()
                    if value is not None
                }
                generated_rfps = SubmittedRFP.objects.filter(**params)
                serializer = SubmittedRFPSerializer(generated_rfps, many=True)
                response = api_response(
                    serializer.data,
                    "success",
                    message="Generated RFP retrieved successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            generated_rfps = SubmittedRFP.objects.all()
            serializer = SubmittedRFPSerializer(generated_rfps, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Generated RFP retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = SubmittedRFPSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Generated RFP created successfully",
                    status_code=200,
                )
                return Response(response, status=200)

            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)

        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class SubmittedRFPListCreateAPIView(ListCreateAPIView):
    queryset = SubmittedRFP.objects.all()
    serializer_class = SubmittedRFPSerializer

    def get(self, request, *args, **kwargs):
        try:
            submitted_rfps = SubmittedRFP.objects.all()
            serializer = SubmittedRFPSerializer(submitted_rfps, many=True)
            response = api_response(
                serializer.data, "success", "Submitted RFPs retrieved successfully", 200
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = SubmittedRFPSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    "Submitted RFP created successfully",
                    200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class SubmittedRFPDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SubmittedRFP.objects.all()
    serializer_class = SubmittedRFPSerializer

    def get(self, request, *args, **kwargs):
        try:
            submitted_rfp = SubmittedRFP.objects.get(pk=kwargs["pk"])
            serializer = SubmittedRFPSerializer(submitted_rfp)
            response = api_response(
                serializer.data,
                "success",
                "Submitted RFP retrieved successfully",
                200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
        return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            submitted_rfp = SubmittedRFP.objects.get(pk=kwargs["pk"])
            serializer = SubmittedRFPSerializer(submitted_rfp, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    [serializer.data],
                    "success",
                    "Submitted RFP updated successfully",
                    200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            submitted_rfp = SubmittedRFP.objects.get(pk=kwargs["pk"])
            submitted_rfp.delete()
            response = api_response(
                None, "success", "Submitted RFP deleted successfully", 200
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)

            return Response(response, status=500)


@api_view(["POST"])
def accept_proposal(request):
    try:
        id = request.data["id"]
        data = SubmittedRFP.objects.get(rfp_id=id)
        data.status = "accepted"
        data.save()
        response = api_response(None, "success", "Proposal accepted successfully", 200)
        return Response(response, status=200)
    except Exception as e:
        response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
        return Response(response, status=500)


@api_view(["POST"])
def reject_proposal(request):
    try:
        id = request.data["id"]
        data = SubmittedRFP.objects.get(rfp_id=id)
        data.status = "rejected"
        data.save()
        response = api_response(None, "success", "Proposal rejected successfully", 200)
        return Response(response, status=200)
    except Exception as e:
        response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
        return Response(response, status=500)


class ProviderListCreateAPIView(ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def get(self, request, *args, **kwargs):
        try:
            providers = Provider.objects.all()
            serializer = ProviderSerializer(providers, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Providers retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = ProviderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Provider created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:

                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:

            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class ProviderDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def get(self, request, *args, **kwargs):
        try:
            provider = Provider.objects.get(pk=kwargs["pk"])
            serializer = ProviderSerializer(provider)
            response = api_response(
                [serializer.data],
                "success",
                message="Provider retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            provider = Provider.objects.get(pk=kwargs["pk"])
            serializer = ProviderSerializer(provider, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    [serializer.data],
                    "success",
                    message="Provider updated successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            provider = Provider.objects.get(pk=kwargs["pk"])
            provider.delete()
            response = api_response(
                None,
                "success",
                message="Provider deleted successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


class SendProposalAPIView(APIView):
    def post(self, request, *args, **kwargs):
        selected_providers = request.data.get("selected_providers_emails", [])
        rfp_id = request.data.get("rfp_id", "")
        mail_service = EmailJSService()
        providers = Provider.objects.filter(contact_email__in=selected_providers)
        for provider in providers:
            mail_service.send_proposal_email(
                provider.contact_email, provider.contact_name
            )

        return Response(
            api_response(None, "success", "Proposals sent successfully", 200),
            status=200,
        )


class ChatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get("prompt", "")
        response = ChatService.process_prompt(prompt)
        resukt = api_response(
            {
                "response": response.get("answer", ""),
                "rfp": {"sections": response.get("rfp_sections", {})},
            },
            "success",
            "Chat response retrieved successfully",
            200,
        )
        return Response(resukt, status=200)


class GetInformationFromWebsiteAPIView(APIView):
    def post(self, request, *args, **kwargs):
        url = request.data.get("url", "")
        information = ChatService.get_information_from_website(url)
        response = api_response(
            information.get("answer", ""),
            "success",
            "Information retrieved successfully",
            200,
        )
        return Response(response, status=200)


class RefactorInformationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        information = request.data.get("information", "")
        refactored_information = ChatService.refactor_information(information)

        response = api_response(
            refactored_information.get("answer", ""),
            "success",
            "Information refactored successfully",
            200,
        )
        return Response(response, status=200)


class OutsetaSupportAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            # Extract data from request
            subject = request.data.get("Subject", "")
            body = request.data.get("Body", "")
            from_person_uid = request.data.get("FromPerson", {}).get("Uid", "")
            source = request.data.get("Source", 2)  # Default to EMAIL (2)
            print(subject, body, from_person_uid, source)

            # Validate required fields
            if not subject or not body or not from_person_uid:
                return Response(
                    api_response(
                        None,
                        "error",
                        "Missing required fields: subject, body, or fromPersonUid",
                        400,
                    ),
                    status=400,
                )

            # Prepare support case data
            support_data = {
                "FromPerson": {"Uid": from_person_uid},
                "Subject": subject,
                "Body": body,
                "Source": source,
            }

            # Initialize Outseta service and create support case
            outseta_service = OutsetaService()
            support_service = outseta_service.SupportService()
            result = support_service.add_case(support_data, send_auto_responder=True)

            if result:
                return Response(
                    api_response(
                        None, "success", "Support request submitted successfully", 200
                    ),
                    status=200,
                )
            else:
                return Response(
                    api_response(
                        None, "error", "Failed to submit support request", 500
                    ),
                    status=500,
                )

        except Exception as e:
            return Response(
                api_response(
                    None, "error", f"Error processing support request: {str(e)}", 500
                ),
                status=500,
            )


class DashboardAPIView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.query_params.get("user_id")
            active_rfx_count = GeneratedRFP.objects.filter(
                user_id=user_id, status="active", end_date__isnull=False
            ).count()

            provider_count = Provider.objects.count()

            return Response(
                api_response(
                    {
                        "active_rfx_count": active_rfx_count,
                        "provider_count": provider_count,
                    },
                    "success",
                    "Active RFX count and provider count retrieved successfully",
                    200,
                ),
                status=200,
            )
        except Exception as e:
            return Response(
                api_response(
                    None,
                    "error",
                    f"Error retrieving active RFX count and provider count: {str(e)}",
                    500,
                ),
                status=500,
            )


class SupportTicketsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.query_params.get("user_id")
            user_email = request.query_params.get("email")

            if not user_email:
                from authentication.models import User

                try:
                    user = User.objects.get(id=user_id)
                    user_email = user.email
                except User.DoesNotExist:
                    return Response(
                        api_response(None, "error", "User not found", 404),
                        status=404,
                    )

            # Initialize Outseta Support Service
            from requestforproposalbackend.services.outseta import OutsetaService

            support_service = OutsetaService.SupportService()

            # Get tickets by user email
            tickets = support_service.get_cases_by_person_email(user_email)

            if tickets is None:
                return Response(
                    api_response(
                        None,
                        "error",
                        "Failed to retrieve support tickets from Outseta",
                        500,
                    ),
                    status=500,
                )

            # Format the response data
            formatted_tickets = []
            for ticket in tickets.get("items", []):
                formatted_ticket = {
                    "id": ticket.get("Uid"),
                    "subject": ticket.get("Subject"),
                    "description": ticket.get("Description"),
                    "status": "open" if ticket.get("Status") == 1 else "closed",
                    "created_at": ticket.get("CreatedDateTime"),
                    "updated_at": ticket.get("UpdatedDateTime"),
                    "messages": [],
                }

                # Add replies if available
                if "Replies" in ticket and ticket["Replies"]:
                    for reply in ticket["Replies"]:
                        formatted_ticket["messages"].append(
                            {
                                "id": reply.get("Uid"),
                                "content": reply.get("Comment"),
                                "user_name": reply.get("AgentName", "Support Agent"),
                                "is_staff": True,
                                "created_at": reply.get("CreatedDateTime"),
                            }
                        )

                formatted_tickets.append(formatted_ticket)

            return Response(
                api_response(
                    formatted_tickets,
                    "success",
                    "Support tickets retrieved successfully",
                    200,
                ),
                status=200,
            )
        except Exception as e:
            return Response(
                api_response(
                    None, "error", f"Error retrieving support tickets: {str(e)}", 500
                ),
                status=500,
            )
