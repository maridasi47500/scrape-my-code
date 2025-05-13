require "test_helper"

class SearchControllerTest < ActionDispatch::IntegrationTest
  test "should get posts" do
    get search_posts_url
    assert_response :success
  end
end
