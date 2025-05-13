require "test_helper"

class WelcomeControllerTest < ActionDispatch::IntegrationTest
  test "should get search" do
    get welcome_search_url
    assert_response :success
  end
end
