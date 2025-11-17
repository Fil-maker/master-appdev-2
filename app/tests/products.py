import pytest
from app.models.product_model import ProductCreate, ProductUpdate
from app.repositories.product_repository import ProductRepository


class TestProductRepository:
    @pytest.mark.asyncio
    async def test_create_product(self, product_repository: ProductRepository):
        """Test создания продукта в репозитории"""
        product_data = {
            "name": "laptop",
        }

        product = await product_repository.create(ProductCreate(**product_data))

        assert product.id is not None
        assert product.name == "laptop"

    @pytest.mark.asyncio
    async def test_update_product(self, product_repository: ProductRepository):
        """Test обновления продукта в репозитории"""
        product_data = {
            "name": "laptop",
        }

        product = await product_repository.create(ProductCreate(**product_data))
        updated_product = await product_repository.update(product.id, ProductUpdate(stock_quantity=12))

        assert updated_product.stock_quantity == 12

    @pytest.mark.asyncio
    async def test_get_list_product(self, product_repository: ProductRepository):
        """Test получение списка продутов в репозитории"""
        product1 = await product_repository.create(ProductCreate(name="laptop"))
        product2 = await product_repository.create(ProductCreate(name="table"))

        products = await product_repository.get_by_filter(2, 1)

        assert len(products) == 2

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repository: ProductRepository):
        """Test получение списка продутов в репозитории"""
        product1 = await product_repository.create(ProductCreate(name="laptop"))
        await product_repository.delete(product1.id)
        deleted_product = await product_repository.get_by_id(product1.id)

        assert deleted_product is None
